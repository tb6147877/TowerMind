import json
import os
from datetime import datetime
from PIL import Image
import base64
import io

def load_data_from_json_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    return loaded_data


def write_data_to_json_file(data, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def set_random_seed(seed):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td_Data/StreamingAssets/Config", "EnvConfig.json")
    # print(file_path)
    data = load_data_from_json_file(file_path)
    data["RandomSeed"]=seed
    write_data_to_json_file(data, file_path)

def set_rl_step_penalty(enabled:bool):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td_Data/StreamingAssets/Config", "EnvConfig.json")
    data = load_data_from_json_file(file_path)
    data["IsDrlReward"]=1 if enabled else 0
    write_data_to_json_file(data, file_path)

def set_only_image_obs(enabled:bool):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td_Data/StreamingAssets/Config", "EnvConfig.json")
    data = load_data_from_json_file(file_path)
    data["IsOnlyPixelObs"]=1 if enabled else 0
    write_data_to_json_file(data, file_path)

def set_target_level(level):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted/linux/td_Data/StreamingAssets/Config", "FixedLevelsConfig.json")
    current_train_level = level
    write_data_to_json_file({'CurrentLevel': current_train_level}, file_path)

def create_one_eval_output_folder():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"eval_output/eval_{timestamp}")

    os.makedirs(folder_path, exist_ok=True)

    return folder_path

def create_one_step_json_file(data,counter,path):

    file_path = os.path.join(path, f"obs_{counter}.json")

    write_data_to_json_file(data, file_path)

def create_one_step_img_file(data,counter,path):

    file_path = os.path.join(path, f"img_{counter}.png")

    #img = Image.fromarray(data).resize((256, 256), resample=Image.BILINEAR)
    img = Image.fromarray(data)

    img.save(file_path)

def encode_image(img):
    img = Image.fromarray(img)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return base64_image