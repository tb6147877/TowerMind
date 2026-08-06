# 📑 TowerMind Documentation (🔥Ongoing Updates)

## 1. General Information

About Environment Basic Settings:
TowerMind is built upon the Unity ML-Agents Toolkit. For more details on customizing features, please refer to the official Unity ML-Agents [documentation](https://github.com/Unity-Technologies/ml-agents).

Observation Space:
Pixel-based (512 x 512 x 3), textual, and structured game-state.

Action Space (Please refer to the following figure):
 X Coordinate $\in$ [-3.0, 3.0], Y Coordinate $\in$ [-3.0, 3.0], Action Type $\in$ {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}. 
For example, the action (-1.5, 1.2, 2) means "construct a Knight Tower at the location on the map with x-coordinate of -1.5 and y-coordinate of 1.2".
<p align="center">
  <img src="assets/environment.png" width="1000">
</p>



## 2. Configuration Table Description

The `td_Data/StreamingAssets/Config` directory under the TowerMind executable contains all configurable files for TowerMind. These files control various utility features and property settings of environment elements. This section provides a detailed explanation of the meaning and usage of each configuration table.


### EnvConfig.json:
1.`GeneralizationLevel`: This field specifies the degree of generalization applied to level selection:
* `0`—FixedLevels: Repeatedly runs the level specified by the `CurrentLevel` field in `FixedLevelsConfig.json`.
* `1`—RandomLevels: Randomly selects a level for each episode from the level-list configuration file specified by `LevelsConfigFileName`.
* `2`—RandomLevelsRandomWaves: Randomly selects a level for each episode from the level-list configuration file specified by `LevelsConfigFileName`. The enemy waves for the selected level are also randomly sampled from `AllWavesConfig.json`.

2.`NeedsNaturalLanguageObservation (Deprecated)`: Whether to enable natural language observations: 0—disabled; 1—enabled. This field was part of an earlier attempt to embed prompts directly in the C# code and is now **deprecated**. Its value should remain set to `0`. Setting it to `1` may prevent the text observation from being generated in a valid JSON format.


3.`NeedsRealtimeLanguageObservation (Deprecated)`: Whether to enable real-time language observations, such as each enemy’s health and position at every environment step: `0`—disabled; `1`—enabled. This feature takes effect only when `NeedsNaturalLanguageObservation` is set to `1`. This field was part of an earlier attempt to embed prompts directly in the C# code and is now **deprecated**. Its value should remain set to `0`. Setting it to `1` may prevent the text observation from being generated in a valid JSON format.

4.`IsOnlyPixelObs`: This field indicates whether the TowerMind environment uses pixel observations exclusively: `0`—no; `1`—yes. To enable text observations, ensure that this field is set to `0`. When only pixel observations are required, setting this field to `1` can improve the environment’s execution speed.

5.`LevelsConfigFileName`: This field specifies the level-list configuration file used by TowerMind. `BenchmarkLevelsConfig.json` contains the nine built-in benchmark levels, while `CustomLevelsConfig.json` provides an example configuration for custom levels.


6.`IsHumanPlayerPlaying`: This field indicates whether TowerMind is being played by a human: `0`—no; `1`—yes. When set to `1`, a user interface designed for human players will be displayed.

7.`IsAutoPlayLevels`: This field specifies whether the system sequentially cycles through all levels listed in the level-list configuration file referenced by `LevelsConfigFileName`: `0`—enabled; `1`—disabled.

8.`IsRepeatFailingLevels`: This field takes effect only when `IsAutoPlayLevels` is set to `1`. It specifies whether the current level should be replayed after a failure: `0`—do not replay; `1`—replay.

9.`PassLevelsRequirement`: This field takes effect only when `IsRepeatFailingLevels` is set to `1`. It specifies the remaining-health threshold used to determine whether a level is completed successfully. If the remaining health at the end of the level is greater than this value, the level is considered successful; otherwise, it is considered failed.

10.`IsDrlReward`: This field specifies whether a step penalty of −0.0005 is applied to the agent at each decision step: `0`—disabled; `1`—enabled.


11.`RoundingDigits`: This field specifies the number of decimal places retained when floating-point state values from TowerMind’s underlying code are included in the text observation. For example, a value of 3 means that the values are rounded to three decimal places.


12.`RandomSeed`: This field specifies the random seed used for running TowerMind. A negative value indicates that a random seed will be generated automatically, while a positive value indicates a user-defined random seed.

13.`DecisionPeriod`: This field is assigned to the `DecisionPeriod` property of the `DecisionRequester` component in [Unity ML-Agents](https://github.com/Unity-Technologies/ml-agents). Please refer to the relevant Unity ML-Agents documentation for further details. In simple terms, this value determines the number of environment steps between two consecutive agent decisions. During the intervening environment steps, the agent does not perform any action. In TowerMind, each environment step corresponds to `0.02` seconds.

14.`GridHNum`: This field takes effect only when `IsDebug` is set to `1`. In debug mode, it is used to display the coordinate grid for TowerMind’s discretized continuous action space. Its value specifies the number of divisions along the x-axis.


15.`GridVNum`: This field takes effect only when `IsDebug` is set to `1`. In debug mode, it is used to display the coordinate grid for TowerMind’s discretized continuous action space. Its value specifies the number of divisions along the y-axis.

16.`IsDebug`: This field controls whether auxiliary information related to action-space discretization is displayed: `1`—enabled; `2`—disabled.


17.`IsRecordingEnabled`: This field primarily specifies whether recording mode is enabled when `IsHumanPlayerPlaying` is set to `1`. Recording mode captures the human player’s action at each environment step, the corresponding JSON-formatted game state, and a video recording of the gameplay.


18.`RecordingPath`: This field specifies the directory in which recording files are stored. Please provide an absolute path. This feature is currently supported only on Windows.


19.`CommonDescription (Deprecated)`: This field provides a general prompt describing the game and is used when `NeedsNaturalLanguageObservation` is set to `1`. This field was part of an earlier attempt to embed prompts directly in the C# code and is now **deprecated**.


20.`Version`: This field is used by developers to record the current version number and does not affect the game’s runtime logic.

### BenchmarkLevelsConfig.json:

This configuration file contains the settings for TowerMind’s built-in benchmark levels. The `Levels` field stores the detailed configuration of each level. Each level is played as a single episode.


1.`ID (Read-only)`: This field serves as the unique identifier of the level within the level-list configuration file. The game uses this field to determine which level to run. Its value must not be duplicated within this file, and users are not advised to modify it.


2.`PicFilePath (Read-only)`: Do not modify this field. It is closely tied to game resource loading, and unauthorized changes may cause runtime errors.


3.`FilePath (Read-only)`: Do not modify this field. It is closely tied to game resource loading, and unauthorized changes may cause runtime errors.


4.`Difficulty (Deprecated)`: This field is deprecated. Modifying its value has no effect, and it is unrelated to the difficulty of the current level.


5.`Waves`: This field is an integer array containing the `ID`s of enemy waves defined in `AllWavesConfig.json`. It specifies which enemy waves are included in the level.

6.`MaxMoney`: This field specifies the maximum number of coins that the player can hold during an episode. Once this limit is reached, collecting additional coins will not increase the player’s coin count.


7.`InitialMoney`: This field specifies the amount of starting funds provided to the player at the beginning of the level.


8.`TotalLife`: This field specifies the player’s total health for the episode. At the beginning of the episode, the player’s current health is initialized to this value. Each time an enemy reaches the player’s base, the player’s health is reduced by one. The episode ends when the player’s health reaches `0`.


9.`WavesInterval`: This field specifies the time interval between two consecutive enemy waves, measured in seconds.


10.`CountdownTime`: This field specifies how many seconds before the next enemy wave begins the countdown is displayed. Its value must be less than `WavesInterval`.




**Note**: 
1. We strongly recommend setting `GeneralizationLevel` to `0` and manually selecting the desired level by modifying the `CurrentLevel` field in `FixedLevelsConfig.json`, as this provides the clearest and simplest configuration workflow.

2. Although this document describes the recording tools provided by TowerMind for human gameplay, we do not recommend relying on them. The recording logic is hard-coded on the C# side, meaning that users cannot inspect or modify its implementation. It therefore functions as a black box from the user’s perspective. In addition, the recorded data were designed specifically to support the experiments presented in the TowerMind paper and may not meet the requirements of other applications. We therefore recommend that users implement their own recording logic to collect the data needed for their specific purposes.





### FixedLevelsConfig.json:
1.`CurrentLevel`: Different benchmark levels can be selected by modifying this field. This field can be used to specify the level only when the `GeneralizationLevel` field in `EnvConfig.json` is set to `0`—FixedLevels. It has no effect when `GeneralizationLevel` is set to any other value. It needs to fill the level `ID` in the level-list configuration file specified by the `LevelsConfigFileName` field in `EnvConfig.json`.




  


## 3. Other Notes:
### 3.1 [Vulkan](https://vulkan.lunarg.com/sdk/home) may need to be installed when CPU rendering is required.

### 3.2 For any configuration-related questions or bug reports, please contact the first author of TowerMind directly.
