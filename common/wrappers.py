import numpy as np
import json
import gym




def get_json_from_obs(obs):
    """
        Interprets an array of ASCII codes (obs) as a string, truncating at
        code==64 ('@'), and parses it into JSON.
    """
    obs1 = np.flip(obs, axis=1)
    ascii_codes = obs1.flatten()
    result = ""
    for code in ascii_codes:
        if code == 64:
            break
        result += chr(code)
    #print(result)
    return json.loads(result)

def get_state_from_obs(obs):
    json = get_json_from_obs(obs)
    # print(json)
    map_center_x = json["Map_Center"]["X"]
    map_center_y = json["Map_Center"]["Y"]
    map_side_length = json["Map_Side_Length"]
    map_l = json["Map_Left_Boundary"]
    map_r = json["Map_Right_Boundary"]

    map_up = json["Map_Upper_Boundary"]
    map_low = json["Map_Lower_Boundary"]
    tower_bounding_w_h = json["Tower_Points_Bounding_Box_Width_Height"]
    gold_coin_collecting_count = json["Level_Gold_Coins_Collection_Count"]
    ff_count = json["Level_Friendly_Fire_Compensation_Count"]

    max_gold_coin = json["Level_Maximum_Gold_Coins"]
    init_health = json["Level_Initial_Health"]
    total_waves = json["Level_Total_Waves_Number"]
    wave_interval = json["Level_Inter_Wave_Interval"]
    selling_tower_rate = json["Level_Selling_Tower_Refund_Rate"]

    gold_coin_refresh_interval = json["Level_Gold_Coins_Refresh_Interval"]
    gold_coin_retention_time = json["Level_Gold_Coins_Retention_Time"]
    gold_coin_min_amount = json["Level_Gold_Coins_Minimum_Pickup_Amount"]
    gold_coin_max_amount = json["Level_Gold_Coins_Maximum_Pickup_Amount"]
    enemy_dest_x = json["Level_Enemy_Destination"]["X"]

    enemy_dest_y = json["Level_Enemy_Destination"]["Y"]
    cur_step = json["Level_Current_Step"]
    cur_time = json["Level_Current_Time"]
    cur_wave = json["Level_Current_Wave"]
    cur_wave_countdown = 0
    try:
        cur_wave_countdown = int(json["Level_Current_Wave_Countdown"])
    except ValueError:
        cur_wave_countdown = 0

    cur_gold_coin = json["Level_Current_Gold_Coins"]
    cur_health = json["Level_Current_Health"]
    remain_waves = json["Level_Remaining_Waves"]
    fow_pos_x = json["Level_Fog_Of_War_Position"]["X"]
    fow_pos_y = json["Level_Fog_Of_War_Position"]["Y"]

    kr_countdown = json["Level_Knight_Reinforcements_Countdown"]
    hero_countdown = json["Level_Hero_Realtime_Status"]["Hero_Revive_Countdown"]
    is_hero_dead = json["Level_Hero_Realtime_Status"]["Is_Hero_Dead"]
    if json["Level_Hero_Realtime_Status"]["Hero_Position"] == None:
        hero_pos_x = -9999.0
        hero_pos_y = -9999.0
    else:
        hero_pos_x = json["Level_Hero_Realtime_Status"]["Hero_Position"]["X"]
        hero_pos_y = json["Level_Hero_Realtime_Status"]["Hero_Position"]["Y"]

    hero_cur_health = json["Level_Hero_Realtime_Status"]["Hero_Current_Health"]
    if json["Level_Dropped_Gold_Coins_Realtime_Status"] == None:
        gold_coin_pos_x = -9999.0
        gold_coin_pos_y = -9999.0
        gold_coin_life_time = -9999.0
    else:
        gold_coin_pos_x = json["Level_Dropped_Gold_Coins_Realtime_Status"]["Position"]["X"]
        gold_coin_pos_y = json["Level_Dropped_Gold_Coins_Realtime_Status"]["Position"]["Y"]
        gold_coin_life_time = json["Level_Dropped_Gold_Coins_Realtime_Status"]["RemainingLifetime"]
    action_x = json["Agent_Last_Action_Info"]["Position"]["X"]

    action_y = json["Agent_Last_Action_Info"]["Position"]["Y"]
    action_index = json["Agent_Last_Action_Info"]["Action_Index"]
    action_is_success = json["Agent_Last_Action_Info"]["Is_Success"]
    action_error = json["Agent_Last_Action_Info"]["Error_Code"]

    paths = []
    for i in range(5):
        if i < len(json["Level_Enemy_Movement_Paths"]):
            for j in range(20):
                if j < len(json["Level_Enemy_Movement_Paths"][i]):
                    paths.append(json["Level_Enemy_Movement_Paths"][i][j]["X"])
                    paths.append(json["Level_Enemy_Movement_Paths"][i][j]["Y"])
                else:
                    paths.append(-9999.0)
                    paths.append(-9999.0)
        else:
            for j in range(20):
                paths.append(-9999.0)
                paths.append(-9999.0)

    cur_wave_e = []
    if json["Level_Current_Wave_Enemies"] == None:
        cur_wave_e = [-9999.0] * 25
    else:
        for i in range(25):
            if i < len(json["Level_Current_Wave_Enemies"]):
                cur_wave_e.append(json["Level_Current_Wave_Enemies"][i])
            else:
                cur_wave_e.append(-9999.0)

    rof_pos = []
    if json["Level_Hero_Fire_Of_Rage_Positions"] == None:
        rof_pos = [-9999.0] * 20
    else:
        for i in range(10):
            if i < len(json["Level_Hero_Fire_Of_Rage_Positions"]):
                rof_pos.append(json["Level_Hero_Fire_Of_Rage_Positions"][i]["X"])
                rof_pos.append(json["Level_Hero_Fire_Of_Rage_Positions"][i]["Y"])
            else:
                rof_pos.append(-9999.0)
                rof_pos.append(-9999.0)

    tower_list = []
    if json["Level_Towers_Realtime_Status"] == None:
        rof_pos = [-9999.0] * 15 * 8
    else:
        for i in range(15):
            if i < len(json["Level_Towers_Realtime_Status"]):
                tower_list.append(json["Level_Towers_Realtime_Status"][i]["Position"]["X"])
                tower_list.append(json["Level_Towers_Realtime_Status"][i]["Position"]["Y"])
                tower_list.append(json["Level_Towers_Realtime_Status"][i]["Tower_Level"])
                tower_list.append(json["Level_Towers_Realtime_Status"][i]["Is_Built"])
                tower_list.append(json["Level_Towers_Realtime_Status"][i]["Is_Frozen"])
                tower_list.append(json["Level_Towers_Realtime_Status"][i]["Knights_Assembly_Position"]["X"])
                tower_list.append(json["Level_Towers_Realtime_Status"][i]["Knights_Assembly_Position"]["Y"])
                if json["Level_Towers_Realtime_Status"][i]["Tower_Name"] == "Archer Tower":
                    tower_list.append(3)
                elif json["Level_Towers_Realtime_Status"][i]["Tower_Name"] == "Magician Tower":
                    tower_list.append(2)
                elif json["Level_Towers_Realtime_Status"][i]["Tower_Name"] == "Knight Tower":
                    tower_list.append(1)
                else:
                    tower_list.append(0)
            else:
                tower_list.append(-9999.0)
                tower_list.append(-9999.0)
                tower_list.append(-9999.0)
                tower_list.append(-9999.0)
                tower_list.append(-9999.0)
                tower_list.append(-9999.0)
                tower_list.append(-9999.0)
                tower_list.append(-9999.0)

    enemies_list = []
    if json["Level_Enemies_Realtime_Status"] == None:
        enemies_list = [-9999.0] * 50 * 4
    else:
        for i in range(50):
            if i < len(json["Level_Enemies_Realtime_Status"]):
                enemies_list.append(json["Level_Enemies_Realtime_Status"][i]["Position"]["X"])
                enemies_list.append(json["Level_Enemies_Realtime_Status"][i]["Position"]["Y"])
                enemies_list.append(json["Level_Enemies_Realtime_Status"][i]["Type"])
                enemies_list.append(json["Level_Enemies_Realtime_Status"][i]["Current_Health"])
            else:
                enemies_list.append(-9999.0)
                enemies_list.append(-9999.0)
                enemies_list.append(-9999.0)
                enemies_list.append(-9999.0)

    knights_list = []
    if json["Level_Knights_Realtime_Status"] == None:
        knights_list = [-9999.0] * 50 * 3
    else:
        for i in range(50):
            if i < len(json["Level_Knights_Realtime_Status"]):
                knights_list.append(json["Level_Knights_Realtime_Status"][i]["Position"]["X"])
                knights_list.append(json["Level_Knights_Realtime_Status"][i]["Position"]["Y"])
                knights_list.append(json["Level_Knights_Realtime_Status"][i]["Current_Health"])
            else:
                knights_list.append(-9999.0)
                knights_list.append(-9999.0)
                knights_list.append(-9999.0)

    obs_vector = np.concatenate([
        [map_center_x, map_center_y, map_side_length, map_l, map_r, map_up, map_low, tower_bounding_w_h
            , gold_coin_collecting_count, ff_count, max_gold_coin, init_health, total_waves, wave_interval,
         selling_tower_rate, gold_coin_refresh_interval
            , gold_coin_retention_time, gold_coin_min_amount, gold_coin_max_amount, enemy_dest_x, enemy_dest_y,
         cur_step, cur_time, cur_wave, cur_wave_countdown
            , cur_gold_coin, cur_health, remain_waves, fow_pos_x, fow_pos_y, kr_countdown, hero_countdown, is_hero_dead,
         hero_pos_x, hero_pos_y, hero_cur_health
            , gold_coin_pos_x, gold_coin_pos_y, gold_coin_life_time, action_x, action_y, action_index,
         action_is_success, action_error],
        paths, cur_wave_e, rof_pos, tower_list, enemies_list, knights_list
    ])

    return obs_vector.astype(np.float32)


def intaction_to_floataction(behaviour):
    index = max(0, min(11, behaviour))  # limited 0~11
    normalized = (index + 0.5) / 12.0  # center of the zone
    return normalized * 2.0 - 1.0  # map to [-1, 1]


class Continuous2DiscreteActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        gym.ActionWrapper.__init__(self, env)

    def action(self, action):
        """Returns a modified action before :meth:`env.step` is called."""
        behaviour = action[2]
        new_behaviour = 0
        new_x = np.clip(action[0] / 3.0, -1, 1)
        new_y = np.clip(action[1] / 3.0, -1, 1)

        new_behaviour = intaction_to_floataction(behaviour)

        new_action = np.array([new_x, new_y, new_behaviour], dtype=np.float32)
        return new_action

    def reverse_action(self, action):
        """Returns a reversed ``action``."""
        print("reverse action")