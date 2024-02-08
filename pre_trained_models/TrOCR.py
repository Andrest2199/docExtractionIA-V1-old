#%%TrOCR
import os
import requests
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
from IPython.display import display


processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')
#%% load image
folder_base_path = os.getcwd()
print (folder_base_path)
folder_base_path= folder_base_path.replace('/pre_trained_models','')
print (folder_base_path)
#%%
image_path = os.path.join(folder_base_path,'0_image_raw/03.jpeg')
image = Image.open(image_path).convert("RGB")

display(image)
image2 = image.crop((20,20,image.size[0]/4,image.size[1]/2))
display(image2)
image01 = image2.crop((0,20,image2.size[0],image2.size[1]/4))
image02 = image2.crop((0,image2.size[1]/4 + 20,image2.size[0],image2.size[1]*2/4))
image03 = image2.crop((0,image2.size[1]*2/4 + 20,image2.size[0],image2.size[1]*3/4))
image04 = image2.crop((0,image2.size[1]*3/4 + 20,image2.size[0],image2.size[1]))
display(image01)
display(image02)
display(image03)
display(image04)
#%%
image_path = os.path.join(folder_base_path,'0_image_raw/01.jpg')
image = Image.open(image_path).convert("RGB")

display(image)
image2 = image.crop((20,20,image.size[0]/4,image.size[1]/2))

image01 = image2.crop((40,image2.size[1]/2,image2.size[0],image2.size[1]))
display(image01)
image02 = image01.crop((130,130,image01.size[0],160))
display(image02)
#%%
pixel_values = processor(images=image02, return_tensors="pt").pixel_values

generated_ids = model.generate(pixel_values)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
print (generated_text)

# %%
