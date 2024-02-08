#%%Layoutlm3
from transformers import AutoProcessor, AutoModelForQuestionAnswering
from datasets import load_dataset
from os import getcwd
from PIL import Image
from IPython.display import display
import torch


processor = AutoProcessor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=True)
model = AutoModelForQuestionAnswering.from_pretrained("microsoft/layoutlmv3-base")

# load document image from the DocVQA dataset
# folder_base_path = getcwd()
# image_path = folder_base_path+'/0_image_raw/01.jpg'
# image = Image.open(image_path).convert("RGB")
dataset = load_dataset("nielsr/funsd-layoutlmv3", split="train")
example = dataset[0]
image = example["image"]
question = "what's his name?"
words = example["tokens"]
boxes = example["bboxes"]
display(image)
encoding = processor(image, question, return_tensors="pt")
start_positions = torch.tensor([1])
end_positions = torch.tensor([3])

outputs = model(**encoding, start_positions=start_positions, end_positions=end_positions)
loss = outputs.loss
start_scores = outputs.start_logits
end_scores = outputs.end_logits
# sequence = processor.batch_decode(outputs.sequences)[0]
# sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
# sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # remove first task start token
# print(sequence)
# print(processor.token2json(sequence))
# %%
