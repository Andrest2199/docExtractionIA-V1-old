#%% LayoutLM
##  pip install pytesseract
##  pip install tesseract
##  pip install tesseract-ocr [no instalado]
import pathlib
from os import getcwd
from transformers import pipeline
folder_base_path = getcwd()
image_path = folder_base_path+'/0_image_raw/01.jpg'

nlp = pipeline(
    "document-question-answering",
    model="microsoft/layoutlmv3-base",
)

nlp(
    image_path,
    "What says under the ramo de seguro field?"
)
# {'score': 0.9943977, 'answer': 'us-001', 'start': 15, 'end': 15}

# %%

