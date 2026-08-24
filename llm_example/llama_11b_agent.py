import requests
import json
import numpy as np
import base64
import os
from llm_example.llm_agent_base import llm_agent_base


class llama_11b_agent(llm_agent_base):
    """
    def __init__(self, name, is_vision: bool, history_length):
        super().__init__(name, is_vision,history_length)
    """

    def _query(self, prompt, image):
        try:
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "llama3.2-vision:11b-instruct-fp16",
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"num_ctx": 20000}
            }) if self.is_vision == False else requests.post("http://localhost:11434/api/generate", json={
                "model": "llama3.2-vision:11b-instruct-fp16",
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "images": [self._encode_64_image(image)],
                "options": {"num_ctx": 20000}
            })
            action = json.loads(response.json()["response"])

            x = max(-3.0, min(self._case_insensitive_get(action, "x", -3.0), 3.0))
            y = max(-3.0, min(self._case_insensitive_get(action, "y", -3.0), 3.0))
            action = max(0, min(self._case_insensitive_get(action, "action", 0), 11))
            return np.array([x, y, action])
        except Exception as e:
            print(f"Error：{str(e)}")
            return np.array([-3.0, -3.0, 6])