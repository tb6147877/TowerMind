from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.envs.unity_gym_env import UnityToGymWrapper
import random
from common.utils import *
from common.wrappers import *
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel
import os

engine_config_channel = EngineConfigurationChannel()
engine_config_channel.set_configuration_parameters(target_frame_rate=-1)
engine_config_channel.set_configuration_parameters(time_scale=20.0)
engine_config_channel.set_configuration_parameters(capture_frame_rate=60)

unity_env = UnityEnvironment(os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td.x86_64"),side_channels=[engine_config_channel])
env = UnityToGymWrapper(unity_env, uint8_visual=True, allow_multiple_obs=True)
env = TowerMindMultiModalObsWrapper(env, use_image=True, use_text=True, use_state=True) # using this wrapper is necessary.
env = TowerMindActionMappingWrapper(env) # using this wrapper is necessary.

set_random_seed(42)
set_target_level(2) # select a level

print("Observation Space:",env.observation_space)
print("Action Space:", env.action_space)

obs=env.reset()
#print(obs["image"]) # Pixel Obs, 512*512*3
#print(obs["text"]) # Text Obs
#print(obs["state"]) # State Obs

done = False

while not done:
    action = env.action_space.sample()
    #print(action)
    obs, _, done, info = env.step(action)
    #print(obs["image"]) # Pixel Obs, 512*512*3
    #print(obs["text"]) # Text Obs
    #print(obs["state"]) # State Obs

env.close()