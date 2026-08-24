
import os

def get_prompt_final_words():
    prompts = "Now please tell me the action you want to perform in this step, in JSON format, containing a floating point X coordinate, a floating point Y coordinate and an integer action index. Your answer should not contain any other text, just provide this json.\n"
    prompts += "\n"
    return prompts

def get_prompt_rule_part():
    prompts = "You are an AI agent playing a video game, you need to build different types of defense towers at different locations on the map to prevent enemies from reaching their destination.\n"
    prompts += "Common rules:\n"
    prompts += "- You need to spend gold coins to build towers, upgrade towers and increase your hero's maximum health. Gold coins will continue to drop at random locations on the map. You can send your knights or hero to pick up gold coins, and the gold coins will be picked up automatically when your knights or hers are near the gold coins.\n"
    prompts += "- If the number of gold coins you hold exceeds the maximum value, the excess will be discarded.\n"
    prompts += "- You will be given a certain amount of health at the beginning of each level. Every time an enemy reaches its destination, you will lose a point of health. When your health reaches 0, the game ends and the mission fails. Try your best to avoid losing any health points.\n"
    prompts += "- Enemies appear in waves, and each level has a different number of enemy waves. There is a certain amount of time between enemy waves. If your health is still greater than 0 after you have resisted all waves of enemy attacks, the mission is successful.\n"
    prompts += "- There are several paths for the enemies, and each enemy will randomly choose one.\n"
    prompts += "- The battlefield of this game is a square area, the details have been included in the level state part blow.\n"
    prompts += "- Between each path point, enemies will only move in a straight line.\n"
    prompts += "- The Fog Of War in the battlefield is an irregular cloud-shaped area that can obscure any element in the game. Its approximate dimensions are 3.5 wide and 1.7 tall. The obscured towers, knights and heroes will no longer attack the enemy, but if the Fog Of War obscures the Fire Of Rage released by the hero, it will lose its obstruction ability during this time.\n"
    prompts += "\n"
    return prompts

def get_prompt_cfg_part():
    file_path_0 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td_Data/StreamingAssets/Config",
                               "TowerConfig.json")
    tower_config = ""
    with open(file_path_0, "r", encoding="utf-8") as file:
        tower_config = file.read()

    file_path_1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td_Data/StreamingAssets/Config",
                               "HeroConfig.json")
    hero_config = ""
    with open(file_path_1, "r", encoding="utf-8") as file:
        hero_config = file.read()

    file_path_2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td_Data/StreamingAssets/Config",
                               "KnightReinforcementsConfig.json")
    knight_reinforcements_config = ""
    with open(file_path_2, "r", encoding="utf-8") as file:
        knight_reinforcements_config = file.read()

    file_path_3 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td_Data/StreamingAssets/Config",
                               "KnightConfig.json")
    knight_config = ""
    with open(file_path_3, "r", encoding="utf-8") as file:
        knight_config = file.read()

    file_path_4 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td_Data/StreamingAssets/Config",
                               "AllEnemiesConfig.json")
    enemies_config = ""
    with open(file_path_4, "r", encoding="utf-8") as file:
        enemies_config = file.read()

    prompts = "The following is the configuration table of each component of the game, organized in Json format:\n"
    prompts += "- Towers Configuration:\n"
    prompts += tower_config
    prompts += "\n"
    prompts += "- Knight Configuration:\n"
    prompts += knight_config
    prompts += "\n"
    prompts += "- Hero Configuration:\n"
    prompts += hero_config
    prompts += "\n"
    prompts += "- Knight Reinforcements Configuration:\n"
    prompts += knight_reinforcements_config
    prompts += "\n"
    prompts += "- Enemies Configuration:\n"
    prompts += enemies_config
    prompts += "\n"
    prompts += "Configuration Table Tips:\n"
    prompts += "- The attack range of the towers, hero, hero's skill and knights is circular, the positions of the circle centers are their position, and the attack range described above is the diameter. When enemies enter this range they will attack.\n"
    prompts += "- The final attack value of the towers, hero, hero's skill, knights and enemies is equal to AttackDamage plus a random value in the range of 0 to AttackExtraDamage.\n"
    prompts += "- The unit of time in this tower defense game is seconds.\n"
    prompts += "- The unit of range or space in this tower defense game is a virtual unified unit. It can be used directly for calculation during reasoning without conversion.\n"
    prompts += "- The AttackSpeed of the towers, hero, knights and enemies refers to the time interval between attacks. For the Knight Tower, it refers to the time interval between summoning knights.\n"
    prompts += "- Upgrading will increase the attack power of the Archer Tower and the Magician Tower, as well as the attack value and movement speed of the knights summoned by the Knight Tower."
    prompts += "\n"
    return prompts

def get_prompt_action_part():
    prompts = "The following are the actions you can take. And for each action, you also need to provide a horizontal and a vertical coordinate between -3.0 and 3.0.\n"
    prompts += "0 - Build an Archer Tower at the coordinates you specify,\n"
    prompts += "1 - Build an Magician Tower at the coordinates you specify,\n"
    prompts += "2 - Build an Knight Tower at the coordinates you specify,\n"
    prompts += "3 - Upgrade a tower at the coordinates you specify,\n"
    prompts += "4 - Sell a tower at the coordinates you specify,\n"
    prompts += "5 - Show the attack range of a tower at the coordinates you specify,\n"
    prompts += "6 - Noop: do nothing,\n"
    prompts += "7 - Change the knights assembly location of a Knight Tower to the coordinates you specify,\n"
    prompts += "8 - Deploy Knight Reinforcements to the coordinates you specify,\n"
    prompts += "9 - Dispatch your hero to the coordinates you specify,\n"
    prompts += "10 - Your hero casts 'Fire of Rage' at your hero's coordinates,\n"
    prompts += "11 - Spend gold coins to increase your hero's maximum health.\n"

    prompts += "Action Tips:\n"
    prompts += "- Building a tower, upgrading a tower or increasing your hero's maximum health requires you to have enough gold coins, otherwise it will be an invalid action.\n"
    prompts += "- Action 0, 1, 2, 3, 4, 5 are only valid if the coordinates you specify are within the bounding box of the tower point. The bounding box of the tower point is a square with its coordinate as the center and a side length of 0.5.\n"
    prompts += "- Action 7 is only valid if the coordinates you specify is within the attack range of a Knight Tower.\n"
    prompts += "- Action 8 will be invalid during the Knight Reinforcements cooldown.\n"
    prompts += "- Action 9 means that your hero starts moving to the coordinates you specify, not a direct teleportation. If you set a new target coordinate during its movement, it will start moving to the new target coordinates.\n"
    prompts += "- Actions 9, 10, 11 are invalid if your hero dies.\n"
    prompts += "- If a tower point already has a tower, you should not build a tower at this tower point, which will result in an invalid action.\n"
    prompts += "- You should provide your action in json format, only three elements in this json structure: \"X\" is a floating point number representing the horizontal coordinate of the action you want to perform; \"Y\" is a floating point number representing the vertical coordinate of the action you want to perform; \"Action\" is an integer representing the index of action you want to perform. \n"
    prompts += "- Action 4 will return the funds spent on its construction and upgrade, but it may not be fully refunded, it depends on the 'Level_Selling_Tower_Refund_Rate' value.\n"

    prompts += "The following are the actions error code list, If you performed an invalid action, you can find out why here:\n"
    prompts += "0 - no error\n"
    prompts += "1 - build a tower where there is already a tower\n"
    prompts += "2 - build a tower but don't have enough gold coins\n"
    prompts += "3 - upgrade a non-existent tower\n"
    prompts += "4 - upgrade a tower but don't have enough gold coins\n"
    prompts += "5 - sell a non-existent tower\n"
    prompts += "6 - failure to provide valid coordinates for building, upgrading, selling a tower or showing the attack range of a tower\n"
    prompts += "7 - failed to provide the valid coordinates for changing the knights assembly location of a Knight Tower\n"
    prompts += "8 - deploy Knight Reinforcements that are on cooldown\n"
    prompts += "9 - try to manipulate a dead hero\n"
    prompts += "10 - increase your hero's maximum health but don't have enough gold coins\n"
    prompts += "11 - show the attack range of a non-existent tower\n"


    prompts += "\n"
    return prompts