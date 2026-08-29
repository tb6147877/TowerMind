import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from typing import Dict, List, Tuple
from gym import spaces

from PIL import Image

from common.wrappers import *
from common.utils import *
from llm_example.llama_11b_agent import *
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.envs.unity_gym_env import UnityToGymWrapper
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel
import matplotlib.pyplot as plt
import io


class ReplayBuffer:
    def __init__(
        self,
        obs_shape,
        size: int,
        batch_size: int = 32
    ):
        self.obs_buf = np.zeros(
            (size, *obs_shape),
            dtype=np.uint8
        )

        self.next_obs_buf = np.zeros(
            (size, *obs_shape),
            dtype=np.uint8
        )

        # Discrete action 应该用整数
        self.acts_buf = np.zeros(
            size,
            dtype=np.int64
        )

        self.rews_buf = np.zeros(
            size,
            dtype=np.float32
        )

        self.done_buf = np.zeros(
            size,
            dtype=np.float32
        )

        self.max_size = size
        self.batch_size = batch_size

        self.ptr = 0
        self.size = 0

    def store(
        self,
        obs: np.ndarray,
        act: int,
        rew: float,
        next_obs: np.ndarray,
        done: bool
    ):
        self.obs_buf[self.ptr] = obs
        self.next_obs_buf[self.ptr] = next_obs

        self.acts_buf[self.ptr] = act
        self.rews_buf[self.ptr] = rew
        self.done_buf[self.ptr] = done

        self.ptr = (self.ptr + 1) % self.max_size
        self.size = min(
            self.size + 1,
            self.max_size
        )

    def sample_batch(self) -> Dict[str, np.ndarray]:

        idxs = np.random.choice(
            self.size,
            size=self.batch_size,
            replace=False
        )

        return dict(
            obs=self.obs_buf[idxs],
            next_obs=self.next_obs_buf[idxs],
            acts=self.acts_buf[idxs],
            rews=self.rews_buf[idxs],
            done=self.done_buf[idxs]
        )

    def __len__(self):
        return self.size



class Network(nn.Module):
    def __init__(
        self,
        in_channels=3,
        num_action_types=12,
        grid_size=10
    ):
        super().__init__()

        self.num_action_types = num_action_types
        self.grid_size = grid_size
        self.num_actions = num_action_types * grid_size * grid_size

        # --------------------------------------------------
        # CNN encoder
        # Input:
        # (B, 3, 128, 128)
        # --------------------------------------------------
        self.encoder = nn.Sequential(

            # (B, 3, 128, 128)
            # ->
            # (B, 32, 64, 64)
            nn.Conv2d(
                in_channels,
                32,
                kernel_size=8,
                stride=2,
                padding=3
            ),
            nn.ReLU(),

            # (B, 32, 64, 64)
            # ->
            # (B, 64, 32, 32)
            nn.Conv2d(
                32,
                64,
                kernel_size=4,
                stride=2,
                padding=1
            ),
            nn.ReLU(),

            # (B, 64, 32, 32)
            # ->
            # (B, 128, 32, 32)
            nn.Conv2d(
                64,
                128,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            nn.ReLU(),

            # (B, 128, 32, 32)
            # ->
            # (B, 256, 32, 32)
            nn.Conv2d(
                128,
                256,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            nn.ReLU(),
        )

        # --------------------------------------------------
        # Convert feature map to exactly 10 × 10
        # --------------------------------------------------
        self.spatial_pool = nn.AdaptiveAvgPool2d(
            (grid_size, grid_size)
        )

        # --------------------------------------------------
        # Spatial Q head
        #
        # (B, 256, 10, 10)
        # ->
        # (B, 128, 10, 10)
        # ->
        # (B, 12, 10, 10)
        #
        # Every spatial position gets 12 Q-values
        # --------------------------------------------------
        self.q_head = nn.Sequential(

            nn.Conv2d(
                256,
                128,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            nn.ReLU(),

            nn.Conv2d(
                128,
                num_action_types,
                kernel_size=1
            )
        )

    def forward(self, x):

        # If image is uint8 [0,255]
        x = x.float() / 255.0

        # CNN features
        x = self.encoder(x)

        # (B, 256, 10, 10)
        x = self.spatial_pool(x)

        # (B, 12, 10, 10)
        q_map = self.q_head(x)

        # --------------------------------------------------
        # Flatten:
        #
        # (B, 12, 10, 10)
        # ->
        # (B, 1200)
        #
        # Compatible with ordinary DQN / Double DQN
        # --------------------------------------------------
        q_values = q_map.permute(
            0, 2, 3, 1
        ).reshape(
            q_map.size(0),
            -1
        )

        return q_values


class DQNAgent:
    def __init__(self, env:gym.Env, memory_size:int, batch_size:int, target_update:int, epsilon_decay:float, seed:int, learning_rate:float, max_epsilon:float=1.0, min_epsilon:float=0.05,gamma:float=0.99, learning_starts = 50_000):
        obs_dim = env.observation_space.shape
        action_dim = env.action_space.n

        self.env = env
        self.memory = ReplayBuffer(obs_dim, memory_size, batch_size)
        self.batch_size = batch_size
        self.epsilon = max_epsilon
        self.epsilon_decay = epsilon_decay
        self.seed = seed
        self.max_epsilon = max_epsilon
        self.min_epsilon = min_epsilon
        self.target_update = target_update
        self.gamma = gamma
        self.learning_starts = learning_starts

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(self.device)

        self.dqn = Network().to(self.device)
        self.dqn_target = Network().to(self.device)
        self.dqn_target.load_state_dict(self.dqn.state_dict())
        self.dqn_target.eval()

        self.optimizer = optim.Adam(self.dqn.parameters(),learning_rate)

        self.transition = list()

        self.is_test=False

    def select_action(self, state:np.ndarray) -> np.ndarray:
        if (not self.is_test) and (np.random.random() < self.epsilon):
            selected_action = self.env.action_space.sample()

        else:
            state_tensor = torch.from_numpy(state).unsqueeze(0).to(self.device)

            with torch.no_grad():
                q_values = self.dqn(state_tensor)
                selected_action = q_values.argmax(dim=1).item()

        if not self.is_test:
            self.transition = [state, selected_action]

        return selected_action

    def step(self, action:np.ndarray) -> Tuple[np.ndarray, np.float64, bool]:
        next_state,reward,done,_ = self.env.step(action)

        if not self.is_test:
            self.transition+=[reward,next_state,done]
            self.memory.store(*self.transition)

        return next_state, reward, done

    def update_model(self)->torch.Tensor:
        samples = self.memory.sample_batch()
        loss = self._compute_dqn_loss(samples)
        self.optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            self.dqn.parameters(),
            max_norm=10.0
        )
        self.optimizer.step()
        return loss.item()

    def train(self,num_frames:int, plotting_interval:int=200):
        self.is_test=False
        state= self.env.reset()
        update_cnt=0
        epsilons=[]
        losses=[]
        scores=[]
        score=0

        for frame_idx in range(1, num_frames+1):
            action = self.select_action(state)
            next_state, reward, done= self.step(action)

            state = next_state
            score += reward

            if done:
                state = self.env.reset()
                scores.append(score)
                print({"step":frame_idx, "score":score})
                score=0

            if frame_idx >= self.learning_starts:
                loss=self.update_model()
                losses.append(loss)
                update_cnt += 1

                self.epsilon =max(self.min_epsilon,self.epsilon-(self.max_epsilon-self.min_epsilon)*self.epsilon_decay)
                epsilons.append(self.epsilon)

                if update_cnt % self.target_update == 0:
                    self._target_hard_update()

            if frame_idx % plotting_interval == 0:
                self._plot(frame_idx,scores,losses,epsilons)


    def test(self, video_folder:str)->None:
        self.is_test=True

        # naive_env=self.env
        # self.env = gym.wrappers.RecordVideo(self.env,video_folder=video_folder)

        state = self.env.reset()
        done=False
        score=0

        while not done:
            action = self.select_action(state)
            next_state, reward, done = self.step(action)
            state = next_state
            score += reward

        print("score:",score)
        #self.env.close()

        #self.env = naive_env

    def _compute_dqn_loss(
            self,
            samples: Dict[str, np.ndarray]
    ) -> torch.Tensor:

        # 保持 uint8，先传 GPU
        state = torch.from_numpy(samples["obs"]).to(self.device)
        next_state = torch.from_numpy(samples["next_obs"]).to(self.device)

        action = torch.from_numpy(
            samples["acts"]
        ).long().unsqueeze(1).to(self.device)

        reward = torch.from_numpy(
            samples["rews"]
        ).float().unsqueeze(1).to(self.device)

        done = torch.from_numpy(
            samples["done"]
        ).float().unsqueeze(1).to(self.device)

        # Q(s,a)
        curr_q_value = self.dqn(state).gather(
            1,
            action
        )

        with torch.no_grad():
            # Double DQN:
            # online network selects
            next_action = self.dqn(
                next_state
            ).argmax(
                dim=1,
                keepdim=True
            )

            # target network evaluates
            next_q_value = self.dqn_target(
                next_state
            ).gather(
                1,
                next_action
            )

            target = (
                    reward
                    + self.gamma
                    * (1.0 - done)
                    * next_q_value
            )

        loss = F.smooth_l1_loss(
            curr_q_value,
            target
        )

        return loss

    def _target_hard_update(self):
        self.dqn_target.load_state_dict(self.dqn.state_dict())



    def _plot(
            self,
            frame_idx: int,
            scores: List[float],
            losses: List[float],
            epsilons: List[float],
    ):
        """Plot the training progress and save it locally."""

        plt.figure(figsize=(20, 5))

        plt.subplot(131)
        plt.title('frame %s. score: %s' % (
            frame_idx,
            np.mean(scores[-10:])
        ))
        plt.plot(scores)

        plt.subplot(132)
        plt.title('loss')
        plt.plot(losses)

        plt.subplot(133)
        plt.title('epsilons')
        plt.plot(epsilons)

        plt.tight_layout()

        plt.savefig(
            "training_progress.png",
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()

seed=42
set_random_seed(seed)
set_target_level(3)
set_rl_step_penalty(True)
set_only_image_obs(True)


engine_config_channel = EngineConfigurationChannel()
engine_config_channel.set_configuration_parameters(target_frame_rate=-1)
engine_config_channel.set_configuration_parameters(time_scale=20.0)
engine_config_channel.set_configuration_parameters(capture_frame_rate=60)
unity_env = UnityEnvironment(os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td.x86_64"),side_channels=[engine_config_channel])


env = UnityToGymWrapper(unity_env, uint8_visual=True, allow_multiple_obs=True)
env = TowerMindMultiModalObsWrapper(env, use_image=True, use_text=False, use_state=False) # using this wrapper is necessary.
env = TowerMindImageBasedRLWrapper(env, behaviour_number=12, split_rate=10, img_shape=(3,128,128), channel_first=True)

print("Observation Space:",env.observation_space)
print("Action Space:", env.action_space)



"""
obs=env.reset()
done = False

#img = np.transpose(obs, (1, 2, 0))
#Image.fromarray(img).save("image.png")


while not done:
    action = env.action_space.sample()
    obs, _, done, info = env.step(action)
"""


def seed_torch(seed):
    torch.manual_seed(seed)
    if torch.backends.cudnn.enabled:
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.deterministic = False

        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
np.random.seed(seed)
seed_torch(seed)



num_frames=2000000
memory_size=500000
batch_size=256
target_update=10000
epsilon_decay=1/300000
learning_rate=1e-4

agent = DQNAgent(env,memory_size,batch_size,target_update,epsilon_decay,seed,learning_rate)

agent.train(num_frames)

video_folder="videos/dqn_double"
agent.test(video_folder)

env.close()