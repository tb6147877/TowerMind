from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.envs.unity_gym_env import UnityToGymWrapper

from common.wrappers import *
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel



engine_config_channel = EngineConfigurationChannel()
engine_config_channel.set_configuration_parameters(target_frame_rate=-1)
engine_config_channel.set_configuration_parameters(time_scale=20.0)
engine_config_channel.set_configuration_parameters(capture_frame_rate=60)

unity_env = UnityEnvironment("/home/dawei/TowerMind/extracted/linux/td.x86_64",side_channels=[engine_config_channel])
env = UnityToGymWrapper(unity_env, uint8_visual=True, allow_multiple_obs=True)
env = Continuous2DiscreteActionWrapper(env)


state=env.reset()
#print(state[0]) # Pixel Obs
#print(get_json_from_obs(state[1])) # Json Obs
print(get_state_from_obs(state[1])) # State Obs

done = False

while not done:
    action = env.action_space.sample()
    state, _, done, info = env.step(action)
    # print(state[0]) # Pixel Obs
    # print(get_json_from_obs(state[1])) # Json Obs
    print(get_state_from_obs(state[1])) # State Obs

env.close()