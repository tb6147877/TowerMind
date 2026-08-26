from collections import deque
import numpy as np
import copy
from common.agent_base import *
from common.utils import *
from llm_example.prompt_util import *

class llm_agent_base(agent_base):
    def __init__(self, name, is_vision:bool, history_length):
        super().__init__(name)
        self.history_length = history_length
        self.history_list = deque(maxlen=self.history_length)
        self.is_vision = is_vision

        self.prompt_rule_part=get_prompt_rule_part()
        self.prompt_action_part=get_prompt_action_part()
        self.prompt_cfg_part=get_prompt_cfg_part()
        self.prompt_final_words=get_prompt_final_words()
        self.format = {
            "type": "object",
            "properties": {
                "X": {
                    "type": "double"
                },
                "Y": {
                    "type": "double"
                },
                "Action": {
                    "type": "integer"
                }
            },
            "required": [
                "X",
                "Y",
                "Action"
            ]
        }


    def _query(self, prompt, image):
        raise NotImplementedError(self.name + " must implement _query()")



    def _combine_prompts(self, obs):
        ori_dict = copy.deepcopy(obs)
        level_dict = {}
        level_dict['Map_Center'] = ori_dict['Map_Center']
        del ori_dict['Map_Center']
        level_dict['Map_Side_Length'] = ori_dict['Map_Side_Length']
        del ori_dict['Map_Side_Length']
        level_dict['Map_Left_Boundary'] = ori_dict['Map_Left_Boundary']
        del ori_dict['Map_Left_Boundary']
        level_dict['Map_Right_Boundary'] = ori_dict['Map_Right_Boundary']
        del ori_dict['Map_Right_Boundary']
        level_dict['Map_Upper_Boundary'] = ori_dict['Map_Upper_Boundary']
        del ori_dict['Map_Upper_Boundary']
        level_dict['Map_Lower_Boundary'] = ori_dict['Map_Lower_Boundary']
        del ori_dict['Map_Lower_Boundary']
        level_dict['Tower_Points_Bounding_Box_Width_Height'] = ori_dict['Tower_Points_Bounding_Box_Width_Height']
        del ori_dict['Tower_Points_Bounding_Box_Width_Height']
        level_dict['Level_Maximum_Gold_Coins'] = ori_dict['Level_Maximum_Gold_Coins']
        del ori_dict['Level_Maximum_Gold_Coins']
        level_dict['Level_Initial_Health'] = ori_dict['Level_Initial_Health']
        del ori_dict['Level_Initial_Health']
        level_dict['Level_Total_Waves_Number'] = ori_dict['Level_Total_Waves_Number']
        del ori_dict['Level_Total_Waves_Number']
        level_dict['Level_Inter_Wave_Interval'] = ori_dict['Level_Inter_Wave_Interval']
        del ori_dict['Level_Inter_Wave_Interval']
        level_dict['Level_Selling_Tower_Refund_Rate'] = ori_dict['Level_Selling_Tower_Refund_Rate']
        del ori_dict['Level_Selling_Tower_Refund_Rate']
        level_dict['Level_Gold_Coins_Refresh_Interval'] = ori_dict['Level_Gold_Coins_Refresh_Interval']
        del ori_dict['Level_Gold_Coins_Refresh_Interval']
        level_dict['Level_Gold_Coins_Retention_Time'] = ori_dict['Level_Gold_Coins_Retention_Time']
        del ori_dict['Level_Gold_Coins_Retention_Time']
        level_dict['Level_Gold_Coins_Maximum_Pickup_Amount'] = ori_dict['Level_Gold_Coins_Maximum_Pickup_Amount']
        del ori_dict['Level_Gold_Coins_Maximum_Pickup_Amount']
        level_dict['Level_Gold_Coins_Minimum_Pickup_Amount'] = ori_dict['Level_Gold_Coins_Minimum_Pickup_Amount']
        del ori_dict['Level_Gold_Coins_Minimum_Pickup_Amount']
        level_dict['Level_Enemy_Movement_Paths'] = ori_dict['Level_Enemy_Movement_Paths']
        del ori_dict['Level_Enemy_Movement_Paths']
        level_dict['Level_Enemy_Destination'] = ori_dict['Level_Enemy_Destination']
        del ori_dict['Level_Enemy_Destination']

        realtime_dict = ori_dict

        result1 = ""
        result1 += self.prompt_rule_part
        result1 += self.prompt_action_part
        result1 += self.prompt_cfg_part
        result1 += "The following is the information about this level, organized in Json format:\n"
        result1 += str(level_dict) + ",\n"
        result1 += "The following is the history of the past few steps, organized in Json format:\n"
        for item in self.history_list:
            result1 += str(item) + ",\n"
        result1 += "The following is the current real-time game status of this step, organized in Json format:\n"
        result1 += str(realtime_dict) + ",\n"
        if self.is_vision:
            result1 += "Image observation provided.\n"
        result1 += self.prompt_final_words

        result2 = str(realtime_dict)

        return (result1, result2)

    def _add_history_item(self, item, action):
        self.history_list.append({"state": item, "action": action})

    def _case_insensitive_get(self,d, key, default):
        for k in d:
            if k.lower() == key.lower():
                return d[k]
        return default

    def _encode_64_image(self,image):
        return encode_image(np.transpose(image.squeeze(), (1,2,0)))


    def act(self, obs):
        self._stat_action_invalid_rate(obs)
        image_obs=obs["image"]
        json_obs=obs["text"]
        temp=self._combine_prompts(json_obs)
        prompt=temp[0]
        action=self._query(prompt,image_obs)
        self._add_history_item(temp[1], action)
        return action

    def clear_level_cache(self):
        self.history_list.clear()
        self.actions_total_num = 0
        self.actions_invalid_num = 0
        self.invalid_action_dict.clear()

    def record_step_data(self, path, obs, counter):
        create_one_step_json_file(obs["text"], counter, path)
        if self.is_vision:
            create_one_step_img_file(np.transpose(obs["image"].squeeze(), (1,2,0)), counter, path)