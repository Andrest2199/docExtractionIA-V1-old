# %%|PRERREQUISITOS PARA INSTALAR TRANSFORMERS|
## [python 3.9 - 3.11]
## conda install pytorch torchvision -c pytorch
## pip install tensorflow
## conda install conda-forge::chardet [necesario con tensorflow]
## pip install --force-reinstall charset-normalizer==3.1.0 [normalmente se instala una version vieja]
## conda install conda-forge::requests
## conda install conda-forge::cmake [si usas MAC M1] No instaladas
## conda install conda-forge::pkg-config [si usas MAC M1] No instaladas
## |
## conda install conda-forge::transformers 4.
## pip install transformers 4.37

# import tensorflow as tf
# import torch
import requests
import pathlib
from os import getcwd
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

folder_base_path = getcwd()
image_path = folder_base_path+'/0_image_raw/01.jpg'
raw_image = Image.open(image_path).convert("RGB")

# conditional image captioning
text =  "The ramo de seguro is"
inputs = processor(raw_image, text, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))

# unconditional image captioning
# inputs = processor(raw_image, return_tensors="pt")

# out = model.generate(**inputs)
# print(processor.decode(out[0], skip_special_tokens=True).strip())

# %%