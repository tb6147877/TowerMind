
import imageio

from common.wrappers import *
from common.utils import *
from llm_example.llama_11b_agent import *
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.envs.unity_gym_env import UnityToGymWrapper
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel
import os

set_random_seed(42)
set_target_level(0)

engine_config_channel = EngineConfigurationChannel()
engine_config_channel.set_configuration_parameters(target_frame_rate=-1)
engine_config_channel.set_configuration_parameters(time_scale=20.0)
engine_config_channel.set_configuration_parameters(capture_frame_rate=60)

unity_env = UnityEnvironment(os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td.x86_64"),side_channels=[engine_config_channel])
env = UnityToGymWrapper(unity_env, uint8_visual=True, allow_multiple_obs=True)
env = TowerMindMultiModalObsWrapper(env, use_image=True, use_text=True, use_state=False) # using this wrapper is necessary.
env = TowerMindActionMappingWrapper(env)  # using this wrapper is necessary.

agent =llama_11b_agent(name="llama_11b_agent",is_vision=True, history_length=3)
output_folder_path = create_one_eval_output_folder()


obs = env.reset()

video_path = os.path.join(output_folder_path, "video.mp4")
writer = imageio.get_writer(video_path, fps=30)
writer.append_data(np.transpose(env.render().squeeze(), (1, 2, 0)))


done = False
total_reward = 0
step_counter=0


while not done:
    action = agent.act(obs)
    obs, reward, done, _ = env.step(action)
    total_reward += reward
    writer.append_data(np.transpose(env.render().squeeze(), (1, 2, 0)))
    agent.record_step_data(output_folder_path, obs, step_counter)
    step_counter = step_counter + 1

writer.close()
print("Reward: "+str(total_reward))
print("Invalid Action Rate: " + str(agent.get_actions_invalid_rate()))

env.close()