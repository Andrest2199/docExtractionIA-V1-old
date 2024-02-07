# %%Blip For QA
import requests
from os import getcwd
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering

processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
folder_base_path = getcwd()
image_path = folder_base_path+'/0_image_raw/03.jpeg'
raw_image = Image.open(image_path).convert("RGB")

question = "What says under the ramo de seguro field?"
inputs = processor(raw_image, question, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))

# %%
