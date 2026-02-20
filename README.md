<h1 align="center">
  <img src="assets/logo.jpg" width="80" />
  TowerMind
</h1>

<p align="center">
  <img src="assets/play_gif.gif" width="500">
</p>

<p align="center">
  <em>GPT-4.1 playing TowerMind.</em>
</p>

# 📖 Introduction
This repository provides the official codebase for the paper "TowerMind: A Tower Defence Game Learning Environment and Benchmark for LLM as Agents." The paper is available on [arXiv](https://arxiv.org/abs/2601.05899). Detailed information and implementation specifics of TowerMind can be found in the paper.

# 📌 News
We are actively improving the documentation to better support researchers using TowerMind. Please keep an eye on this section for future updates.

✅ Documentation updated: How to select different benchmark levels by modifying the configuration.

⬜ Documentation on adjusting base level attributes via configuration files will be released soon. Stay tuned!

# 📦 Getting Started

## 1.Clone the Repo:
```bash
git clone git@github.com:tb6147877/TowerMind.git

cd TowerMind
```

## 2.Extracted the Env:
```bash
unzip compressed_env/linux.zip -d extracted/

chmod +x ./extracted/linux/td.x86_64
```

## 3.1Play as a Human:
```bash
./extracted/linux/td.x86_64
```
For **Windows** users, simply extract windows.zip in `./compressed_env` to get started.

**macOS** versions (for both Apple Silicon and Intel) require two additional steps after extraction in order to run properly on a Mac:
1. Run ```xattr -dr com.apple.quarantine td.app``` in the directory where you extracted the files.

2. Run ```chmod +x YourGame.app/Contents/MacOS/*``` in the same directory.

3. Then, you can launch the app by clicking the icon. If macOS prompts for permissions, go to System Settings > Privacy & Security to allow the app to run.

## 3.2Use as a Gym Env:
```bash
conda create -n towermind python=3.10.12 && conda activate towermind

python -m pip install mlagents==1.1.0

python ./hello_world.py
```

# 📑 Documentation (🔥Ongoing Updates)

Obs Space:
Pixel-Based (512 x 512 x 3), Textual, and Structured Game-State

Action Space (Please refer to the following figure):
 X Coordinate $\in$ [-3.0, 3.0], Y Coordinate $\in$ [-3.0, 3.0], Action Type $\in$ {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}. 
For example, the action (-1.5, 1.2, 2) means "construct a Knight Tower at the location on the map with x-coordinate of -1.5 and y-coordinate of 1.2".
<p align="center">
  <img src="assets/environment.png" width="1000">
</p>

About Env Basic Settings:
TowerMind is built upon the Unity ML-Agents Toolkit. For more details on customizing features, please refer to the official Unity ML-Agents [documentation](https://github.com/Unity-Technologies/ml-agents).

TowerMind Customizability:
Directory`./extracted/linux/td_Data/StreamingAssets/Config`includes all configurable files for TowerMind, which control various utility features and property settings of environment elements.

1. How to select different benchmark levels by modifying the configuration: Different benchmark levels can be selected by modifying the `CurrentLevel` field in the `FixedLevelsConfig` file. Valid values are integers ranging from `0` to `8`, meaning that TowerMind provides 9 built-in benchmark levels. Please DO NOT modify the `CustomLevelsConfig` file until the **Level Editor** is officially released.


Possible Problems:
1.[Vulkan](https://vulkan.lunarg.com/sdk/home) may need to be installed when CPU rendering is required.

# 🚀 Roadmap
As our team is currently engaged in other ongoing research projects, this repository is not yet fully polished. However, we will continue to actively maintain and update it.

The **Level Editor** will be released soon.

Please note that the current version of TowerMind already fully supports both LLM-based and RL-based evaluations. 

# 📚 Citation

If you find this work useful, please cite:

```bibtex
@article{wang2026towermind,
  title={TowerMind: A Tower Defence Game Learning Environment and Benchmark for LLM as Agents},
  author={Wang, Dawei and Zhou, Chengming and Zhao, Di and Liu, Xinyuan and Ma, Marci Chi and Ushaw, Gary and Davison, Richard},
  journal={arXiv preprint arXiv:2601.05899},
  year={2026}
}
