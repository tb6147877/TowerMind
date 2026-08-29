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
import io


class ReplayBuffer:
    def __init__(self, obs_dim:int, size:int, batch_size:int=32):
        self.obs_buf = np.zeros([size, obs_dim], dtype=np.float32)
        self.next_obs_buf = np.zeros([size, obs_dim], dtype=np.float32)
        self.acts_buf = np.zeros(size, dtype=np.float32)
        self.rews_buf = np.zeros(size, dtype=np.float32)
        self.done_buf = np.zeros(size, dtype=np.float32)

        self.max_size = size
        self.batch_size = batch_size
        self.ptr=0
        self.size=0

    def store(self, obs:np.ndarray, act:np.ndarray, rew:float, next_obs:np.ndarray, done:bool):
        self.obs_buf[self.ptr] = obs
        self.next_obs_buf[self.ptr] = next_obs
        self.acts_buf[self.ptr] = act
        self.rews_buf[self.ptr] = rew
        self.done_buf[self.ptr] = done

        self.ptr = (self.ptr + 1) % self.max_size
        self.size = min(self.size + 1, self.max_size)

    def sample_batch(self) -> Dict[str, np.ndarray]:
        idxs = np.random.choice(self.size, size=self.batch_size, replace=False)
        return dict(obs=self.obs_buf[idxs],next_obs=self.next_obs_buf[idxs],acts= self.acts_buf[idxs],rews=self.rews_buf[idxs],done=self.done_buf[idxs])

    def __len__(self) -> int:
        return self.size


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

set_random_seed(42)
set_target_level(0)

obs=env.reset()
done = False


#img = np.transpose(obs, (1, 2, 0))
#Image.fromarray(img).save("image.png")


while not done:
    action = env.action_space.sample()
    obs, _, done, info = env.step(action)

env.close()