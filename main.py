# %% Import libraries
import json
from image_pre_procesing import (
    process_images,
    identify_file,
    get_images_from_pdf,
    pdf_has_text,
    get_text_from_pdf,
    convert_pdf_to_image
)
from improve_image_quality import improve_image_quality
from ocr_openai_vision import ocr_openai_vision
from ocr_google_vision import ocr_google_vision
from cleaning_extract_process import json_extraction, txt_extraction
from ocr_openai_chat_completion import chat_completion_cleaning
from utils.file_utils import FileUtils
import os
# from entity_recognition_openai import recognition_openai
from ocr_aws_textract import extract_text_from_image, anlyse_text_and_create_dict


# %% Set the paths

folder_base_path = os.getcwd()
image_raw_folder = os.path.join(folder_base_path, "0_image_raw")
image_preprocessed_folder = os.path.join(folder_base_path, "1_image_preprocessed")
image_improved_folder = os.path.join(folder_base_path, "2_image_improved")
text_extracted_folder = os.path.join(folder_base_path, "3_text_extracted")
results_folder = os.path.join(folder_base_path, "4_results")
data_inject_folder = os.path.join(folder_base_path, "data_inject")


def process_text_file(text_file, doctype, extraction_method=str):
    text_file = os.path.join(text_extracted_folder, text_file)
    filename = os.path.basename(text_file)


    text_file_path = os.path.join(text_extracted_folder, text_file)
    if text_file.endswith(".txt"):
        file_content = FileUtils.read(text_file_path)
    
        # regex method
        if extraction_method == "txt_extraction":
            extracted_text = txt_extraction(file_content, doctype)
            extracted_text = json.dumps(
                extracted_text, ensure_ascii=True, indent=2, sort_keys=True
            )

        # chat completions method
        elif extraction_method == "chat_completions":
            extracted_text = chat_completion_cleaning(
                text_file, results_folder, data_inject_folder + "/" + doctype, doctype
            )
        extracted_text = json.dumps(extracted_text)


    elif text_file.endswith(".json"):
        file_content = FileUtils.read(text_file_path)
        if extraction_method == "json_extraction":
            # data_cleaned = data_cleaning(file_content)
            extracted_text = json_extraction(file_content, doctype)
            extracted_text = json.dumps(
                extracted_text, ensure_ascii=True, indent=2, sort_keys=True
            )
        elif extraction_method == "chat_completions":
            extracted_text = chat_completion_cleaning(
                text_file, results_folder, data_inject_folder + "/" + doctype, doctype
            )
        extracted_text = json.dumps(extracted_text)
            
        
    return file_content, extracted_text, extraction_method


def process_image_files(procesed_images_list, ocr_method=str):
    for image in procesed_images_list:

        images_path = os.path.join(image_preprocessed_folder, image)
        # improve image quality
        # improve_image_quality(images_path, os.path.join(image_improved_folder, image))
        print("Processing improved image: ", image)
        improve_image_quality(images_path, image_improved_folder)
    improved_images_list = FileUtils.create_list(image_improved_folder)

    for image in improved_images_list:

        # apply ocr openai vision
        images_path = os.path.join(image_improved_folder, image)
        if ocr_method == "openai":
            ocr_openai_vision(
                images_path,
                text_extracted_folder,
            )

        # apply ocr google vision
        if ocr_method == "google":
            ocr_google_vision(images_path, text_extracted_folder)
        # ocr_google_vision(images_path, text_extracted_folder)

        if ocr_method == "aws_textract":
            text_corpus = extract_text_from_image(images_path)
            FileUtils.save(
                text_extracted_folder + "/" + "_AWS_extract.txt", text_corpus
            )
        if ocr_method == "aws_parser":
            fields = anlyse_text_and_create_dict(images_path)
            FileUtils.save(
                text_extracted_folder + "/" + "_AWS_analyzed.json",
                json.dumps(fields, ensure_ascii=True, indent=2, sort_keys=True),
            )


def document_handler(file_path=str, doctype=str, ocr_method=str):
    file_name = os.path.basename(file_path)
    filetype = identify_file(file_name)

    if filetype == "pdf":
        has_text = pdf_has_text(file_path)
        if has_text:
            print("Digital pdf")
            text_corpus = get_text_from_pdf(file_path)
            new_file_name = file_name.strip(".pdf") + ".txt"

            text_extracted = FileUtils.save(
                text_extracted_folder + "/" + new_file_name, text_corpus
            )

            return ocr_method

        else:
            print("Images inside PDF, retrieving images...")
            # images_in_pdf = get_images_from_pdf(file_path, image_preprocessed_folder)
            convert_pdf_to_image(file_path, image_preprocessed_folder)
            images_in_pdf = FileUtils.create_list(image_preprocessed_folder)
            process_image_files(images_in_pdf, ocr_method)
            

            return ocr_method
    else:
        print("File is an Imagetype ")
        process_images(file_path, image_preprocessed_folder)
        procesed_images_list = FileUtils.create_list(image_preprocessed_folder)
        process_image_files(procesed_images_list, ocr_method)
        return ocr_method


# %% Main function
def main(file_path=str, doctype=str) -> dict:
    if doctype not in ["IMSS", "INFONAVIT", "SAT"]:
        raise ValueError(
            "Document type not recognized. Please provide a valid document type: IMSS, INFONAVIT, SAT"
        )

    data = {
        "name": os.path.basename(file_path),
        "content": doctype,
        "entity_recognition": "",
        "ocr": "",
        "values": {},
    }

    methods = ["openai", "google", "aws_textract", "aws_parser"]
    for method in methods:
        FileUtils.delete_from_folder(text_extracted_folder)
        ocr = document_handler(file_path, doctype, method)
        all_text_files = FileUtils.list_text_files(text_extracted_folder)

        for text_file in all_text_files:
            print("text file", text_file)
            if text_file.endswith(".txt"):
                entity_methods = [
                    "txt_extraction",
                    "chat_completions",
                ]

                for entity_method in entity_methods:

                    raw_text, values, recognition = process_text_file(
                        text_file, doctype, entity_method
                    )
                    data["plain text"] = raw_text
                    data["values"] = values
                    data["ocr"] = ocr
                    data["entity_recognition"] = recognition
                    FileUtils.save(
                        f"{results_folder}/{data['name'][:-4]}_{data['ocr']}_{data['entity_recognition']}.json",
                        json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True),
                    )
            elif text_file.endswith(".json"):
                entity_methods = [
                    "json_extraction",
                    "chat_completions",
                ]
                for entity_method in entity_methods:
                    raw_text, values, recognition = process_text_file(
                        text_file, doctype, entity_method
                    )
                    data["plain text"] = raw_text
                    data["values"] = values
                    data["ocr"] = ocr
                    data["entity_recognition"] = recognition
                    FileUtils.save(
                        f"{results_folder}/{data['name'][:-4]}_{data['ocr']}_{data['entity_recognition']}.json",
                        json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True),
                    )
        #TODO: call process to get system_accuracy forloop
    return data


def clean_folders():
    FileUtils.delete_from_folder(image_preprocessed_folder)
    FileUtils.delete_from_folder(image_improved_folder)
    FileUtils.delete_from_folder(text_extracted_folder)
    FileUtils.delete_from_folder(results_folder)


# %% Run main function
if __name__ == "__main__":
    # Remove files for all output folders
    FileUtils.delete_from_folder(results_folder)
    FileUtils.delete_from_folder(image_preprocessed_folder)
    FileUtils.delete_from_folder(image_improved_folder)

    """

    # get the list of files unprocessed for IMSS
    raw_imss_list = FileUtils.create_list(os.path.join(image_raw_folder, "IMSS"))
    # get the file paths for every image inside imss folder
    imss_files_path = os.path.join(image_raw_folder, "IMSS")
    # get the original names of the files
    imss_original_names = FileUtils.get_original_names(imss_files_path)

    for file in raw_imss_list:
        file = os.path.join(imss_files_path, file)
        main(file, "IMSS")
    """

    # get the list of file unprocessed for INFONAVIT
    raw_infonavit_list = FileUtils.create_list(
        os.path.join(image_raw_folder, "INFONAVIT")
    )
    # get the file paths for every image inside the infonavit folder
    infonavit_file_paths = os.path.join(image_raw_folder, "INFONAVIT")
    for file in raw_infonavit_list:
        file = os.path.join(infonavit_file_paths, file)
        main(file, "INFONAVIT")
    # get the list of file unprocessed for INFONAVIT
    raw_sat_list = FileUtils.create_list(os.path.join(image_raw_folder, "SAT"))
    # get the file paths for every image inside the infonavit folder
    sat_file_paths = os.path.join(image_raw_folder, "SAT")
    for file in raw_sat_list:
        file = os.path.join(sat_file_paths, file)
        main(file, "SAT")


# %%
