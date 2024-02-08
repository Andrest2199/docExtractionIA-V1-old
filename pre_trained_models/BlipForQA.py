# %%Blip For QA
import requests
import os
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering
# %%
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

folder_base_path = os.getcwd()
image_path = os.path.join(folder_base_path,'0_image_raw/01.jpg')
raw_image = Image.open(image_path).convert("RGB")

question = "What says under the ramo de seguro field?"
question2 = "Provide the text below 'ramo de seguro'"
question3 = "Provide the start date"
inputs = processor(raw_image, question2, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))

# %%
