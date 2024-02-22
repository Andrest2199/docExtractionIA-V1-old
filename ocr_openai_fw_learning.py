# %% openai vision
import json
import utils
import os
from openai import OpenAI

# OpenAI API Key
OpenAI.api_key = os.environ["OPENAI_API_KEY"]

"""
DOCS:
https://platform.openai.com/docs/guides/vision

TODO:
1) Modify prompt to include a few examples of desired output
"""


# %% Define functions
def ocr_openai_vision(image_path, output_folder, data_inject_folder):
    # Set Data for system from folder 'Data inject'
    user_prompt = []
    context_data_inyection = ""
    input_json_list = []
    input_document_list = []
    doc_count = 0
    json_count = 0
    # Retrieve files from 'Data Inject'
    all_data_inject_files = utils.create_file_list(data_inject_folder)
    for file in all_data_inject_files:
        if file.endswith(".txt"):
            input_json_list.append(
                utils.read_file(os.path.join(data_inject_folder, file))
            )
            json_count += 1
        elif file.endswith(".jpeg") or file.endswith(".jpg"):
            base64_image = utils.encode_image(os.path.join(data_inject_folder, file))
            input_document_list.append(f"data:image/jpeg;base64,{base64_image}")
            doc_count += 1

    # Set context data
    context_data_inyection=f"Here are examples of {doc_count} image and {json_count} text string extracted from the images"

    # Set user context prompt
    user_prompt.append({"type": "text","text": context_data_inyection})
    
    # Inject context data json/txt to the user prompt
    for input_json in input_json_list:
        user_prompt.append({"type": "text","text":str(input_json)})

    # Inject context data documents/images to the user prompt
    for input_doc in input_document_list:
        user_prompt.append({"type": "image_url","image_url":{"url":input_doc},"detail":"low"})
        # user_prompt.append({"type": "image_url","image_url":{"url":"https://dm.grupoono.lat/index.php/apps/files_sharing/publicpreview/bQf8FkHPcxZpwG5?file=/&fileId=48868&x=2880&y=1800&a=true&etag=45310a2b33c267f45df430355a776da2"},"detail":"low"})
        # break
    # print(f"Context User Prompt: {user_prompt}")

    print(f"Processing image: {image_path}")
    # Getting the base64 string
    base64_image = utils.encode_image(image_path)
    # Image URL
    image = f"data:image/jpeg;base64,{base64_image}"
    # Set desire user request
    user_prompt.append({"type": "text",
                    "text": "Create and return a JSON with the data in the next image"})
    # Set desire user image request
    user_prompt.append({"type": "image_url", 
                    "image_url": {"url": image}})
    
    # Numero de tokens usados
    # num_tokens = utils.num_tokens_from_messages(user_prompt,"gpt-4-vision-preview")
    # print (f"Tokens in User Prompt: {num_tokens}")

    # print(f"Final User Prompt: {json.dumps(user_prompt,ensure_ascii=False,indent=2)}")
    user_prompt = str(user_prompt)
    
    # Create instance of openAI client
    client = OpenAI()

    # Get response
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",  # gpt-3.5-turbo-0125 #gpt-4-0125-preview, #gpt-4-vision-preview
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        max_tokens=2000,
    )

    # Extract json content from response
    json_string = response.choices[0].message.content
    json_string = json_string.replace("```json\n", "").replace("\n```", "")

    # Save json data
    print(json_string)
    json_data = json.loads(json_string)
    file_extension = image_path.split(".")[-1]
    json_file_name = image_path.split("/")[-1].replace(f".{file_extension}", ".json")

    with open(output_folder + "/" + json_file_name, "w") as file:
        json.dump(json_data, file, indent=4)

    tokens_count_by_gpt = response.usage.prompt_tokens
    print(f'Tokens Count by API: {tokens_count_by_gpt}')

# %% TEST
folder_base_path = os.getcwd()
image_improved_folder = folder_base_path + "/2_image_improved"
text_extracted_folder = folder_base_path + "/3_text_extracted"
data_inject_folder = folder_base_path + "/data_inject"

test_file = os.path.join(image_improved_folder, "7_procesed.jpeg")

ocr_openai_vision(test_file, text_extracted_folder, data_inject_folder)
#%%