# %% openai vision

import base64
import json

import os
from openai import OpenAI

# OpenAI API Key
OpenAI.api_key = os.environ["OPENAI_API_KEY"]

# Get base path
folder_base_path = os.getcwd()

"""
DOCS:
https://platform.openai.com/docs/guides/vision

TODO:
1) Modify prompt to include a few examples of desired output
"""

# %% Encode image

# Define function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = folder_base_path + "/1_image_procesed/0_procesed.jpeg"

# Getting the base64 string
base64_image = encode_image(image_path)

# Image URL
image_url = f"data:image/jpeg;base64,{base64_image}"

# %% Send image to GPT 4 vision

# Create instance of openAI client
client = OpenAI()

# Get response
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Return JSON document with data. Only return JSON not other text.",
                },
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        }
    ],
    max_tokens=2000,
)

# Extract json content from response
json_string = response.choices[0].message.content
json_string = json_string.replace("```json\n", "").replace("\n```", "")

# Save json data
json_data = json.loads(json_string)
json_file_name = "0_text.json"

with open(folder_base_path + '/4_results/' + json_file_name, 'w') as file:
  json.dump(json_data, file, indent=4)

# %%
