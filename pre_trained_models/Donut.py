#%% Donut
##  conda install conda-forge::sentencepiece 
##  pip install datasets
import re
import torch
from os import getcwd
from PIL import Image
from transformers import DonutProcessor, VisionEncoderDecoderModel
from datasets import load_dataset
#%%
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
# load document image from the DocVQA dataset
folder_base_path = getcwd()
image_path = folder_base_path+'/0_image_raw/01.jpg'
image = Image.open(image_path).convert("RGB")

# prepare decoder inputs
task_prompt = "<s_docvqa><s_question>{user_input}</s_question><s_answer>"
question = "What is the ramo de seguro?"
prompt = task_prompt.replace("{user_input}", question)
decoder_input_ids = processor.tokenizer(prompt, add_special_tokens=False, return_tensors="pt").input_ids

pixel_values = processor(image, return_tensors="pt").pixel_values

outputs = model.generate(
    pixel_values.to(device),
    decoder_input_ids=decoder_input_ids.to(device),
    max_length=model.decoder.config.max_position_embeddings,
    pad_token_id=processor.tokenizer.pad_token_id,
    eos_token_id=processor.tokenizer.eos_token_id,
    use_cache=True,
    bad_words_ids=[[processor.tokenizer.unk_token_id]],
    return_dict_in_generate=True,
)

sequence = processor.batch_decode(outputs.sequences)[0]
sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # remove first task start token
print(processor.token2json(sequence))
# %%
