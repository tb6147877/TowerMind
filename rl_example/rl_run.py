import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from typing import Dict, List, Tuple
from gym import spaces

from common.wrappers import *
from common.utils import *
from llm_example.llama_11b_agent import *
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.envs.unity_gym_env import UnityToGymWrapper
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel
import io

engine_config_channel = EngineConfigurationChannel()
engine_config_channel.set_configuration_parameters(target_frame_rate=-1)
engine_config_channel.set_configuration_parameters(time_scale=20.0)
engine_config_channel.set_configuration_parameters(capture_frame_rate=60)
unity_env = UnityEnvironment(os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td.x86_64"),side_channels=[engine_config_channel])


env = UnityToGymWrapper(unity_env, uint8_visual=True, allow_multiple_obs=True)
env = TowerMindMultiModalObsWrapper(env, use_image=True, use_text=False, use_state=False) # using this wrapper is necessary.
env = TowerMindActionMappingWrapper(env)  # using this wrapper is necessary.

print("Observation Space:",env.observation_space)
print("Action Space:", env.action_space)

env.close()