
import imageio

from common.wrappers import *
from common.utils import *
from llm_example.llama_11b_agent import *
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.envs.unity_gym_env import UnityToGymWrapper
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel





engine_config_channel = EngineConfigurationChannel()
engine_config_channel.set_configuration_parameters(target_frame_rate=-1)
engine_config_channel.set_configuration_parameters(time_scale=20.0)
engine_config_channel.set_configuration_parameters(capture_frame_rate=60)
unity_env = UnityEnvironment("/home/[your user name]/TowerMind/extracted/linux/td.x86_64",side_channels=[engine_config_channel])


env = UnityToGymWrapper(unity_env, uint8_visual=True, allow_multiple_obs=True)
env = MultiModalObsWrapper(env)
env = Continuous2DiscreteActionWrapper(env)

agent =llama_11b_agent(name="llama_11b_agent",is_vision=True, history_length=3)
output_folder_path = create_one_eval_output_folder()
set_random_seed(42)
set_target_level(0)

state = env.reset()
#state=(state[0], get_json_from_obs(state[1]))
video_path = os.path.join(output_folder_path, "video.mp4")
writer = imageio.get_writer(video_path, fps=30)
writer.append_data(np.transpose(env.render().squeeze(), (1, 2, 0)))


done = False
total_reward = 0
step_counter=0


while not done:
    action = agent.act(state)
    state, reward, done, _ = env.step(action)
    #state = (state[0], get_json_from_obs(state[1]))
    total_reward += reward
    writer.append_data(np.transpose(env.render().squeeze(), (1, 2, 0)))
    agent.record_step_data(output_folder_path, state, step_counter)
    step_counter = step_counter + 1

writer.close()
print("Reward: "+str(total_reward))
print("Invalid Action Rate: " + str(agent.get_actions_invalid_rate()))

env.close()