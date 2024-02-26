# %% Import libraries
import json
from image_pre_procesing import (
    process_images,
    identify_file,
    get_images_from_pdf,
    pdf_has_text,
    get_text_from_pdf,
)
from improve_image_quality import improve_image_quality
from ocr_openai_vision import ocr_openai_vision
from ocr_google_vision import ocr_google_vision
from cleaning_extract_process import data_cleaning, data_extraction, regex_extraction
from ocr_openai_chat_completion import openai_recognition
from utils.file_utils import FileUtils
import os

# TODO: Print OCR method inside json file
# %% Set the paths

folder_base_path = os.getcwd()
image_raw_folder = os.path.join(folder_base_path, "0_image_raw")
image_preprocessed_folder = os.path.join(folder_base_path, "1_image_preprocessed")
image_improved_folder = os.path.join(folder_base_path, "2_image_improved")
text_extracted_folder = os.path.join(folder_base_path, "3_text_extracted")
results_folder = os.path.join(folder_base_path, "4_results")
data_inject_folder = os.path.join(folder_base_path, "data_inject")


def process_text_file(text_file, text_extracted_folder, results_folder, doctype):
    if doctype == "IMSS":
        operation = "incapacidades"
    elif doctype == "INFONAVIT":
        operation = "infonavit"
    elif doctype == "SAT":
        operation = "codigos_postales"
    text_file_path = os.path.join(text_extracted_folder, text_file)
    if text_file.endswith(".txt"):
        ocr_method = "google vision"
        file_content = FileUtils.read(text_file_path)
        json_objects = file_content.split(
            "\n"
        )  # assuming each JSON object is on a new line
        json_str = FileUtils.read(text_file_path)
        extracted_text = regex_extraction(json_str)
        extraction_method = "regex"  
        json_str = json.dumps(
            extracted_text,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        FileUtils.save(results_folder + "/" + text_file, json_str)
        return json_str, ocr_method, extraction_method

        # for json_str in json_objects:
        #     if json_str:  # check if the string is not empty
        #         extracted_text = regex_extraction(json_str)
        #         extraction_method = "regex"
        #         json_str = json.dumps(
        #             extracted_text,
        #             ensure_ascii=True,
        #             indent=2,
        #             sort_keys=True,
        #         )
        #         FileUtils.save(results_folder + "/" + text_file, json_str)
                # return json_str, ocr_method, extraction_method
    elif text_file.endswith(".json"):
        ocr_method = "Openai"
        data_cleaned = data_cleaning(text_file)
        extracted_text = data_extraction(data_cleaned, operation)
        extraction_method = "text_extraction"
        return extracted_text, ocr_method, extraction_method


def process_image_files(
    procesed_images_list,
    image_preprocessed_folder,
    image_improved_folder,
    text_extracted_folder,
):
    for image in procesed_images_list:
        images_path = os.path.join(image_preprocessed_folder, image)
        # improve image quality
        improve_image_quality(images_path, os.path.join(image_improved_folder, image))
    improved_images_list = FileUtils.create_list(image_improved_folder)
    for image in improved_images_list:
        # apply ocr openai vision
        images_path = os.path.join(image_improved_folder, image)
        ocr_openai_vision(
            images_path,
            text_extracted_folder,
        )
        # apply ocr google vision
        ocr_google_vision(images_path, text_extracted_folder)

def document_handler(file_path=str, doctype=str, extract_method=str):
    file_name = os.path.basename(file_path)
    filetype = identify_file(file_name)

    if filetype == "pdf":
        has_text = pdf_has_text(file_path)
        if has_text:
            print("file has text inside")
            text_corpus = get_text_from_pdf(file_path)
            new_file_name = file_name.strip(".pdf") + ".txt"
            text_extracted = FileUtils.save(text_extracted_folder + "/" + new_file_name, text_corpus)

            # regex mehtod
            if extract_method == "regex":

                result = regex_extraction(text_extracted)
                json_str = json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True)
                FileUtils.save(results_folder + "/" + new_file_name, json_str)
                method = "text_extraction"
                return method, result, extract_method
            # openai method
            """"
            if extract_method == "openai":
                result = openai_recognition(file_path, text_extracted_folder, data_inject_folder)
                method = "text_extraction"
                return method, result, extract_method
            """
        else:
            print("file does not have text inside")
            get_images_from_pdf(file_path, image_preprocessed_folder)
            procesed_images_list = FileUtils.create_list(image_preprocessed_folder)
            process_image_files(
            procesed_images_list,
            image_preprocessed_folder,
            image_improved_folder,
            text_extracted_folder,
        )
            all_text_files = FileUtils.list_text_files(text_extracted_folder)
                
            for text_file in all_text_files:
                try:
                    text_extracted, ocr_method, method  = process_text_file(
                    text_file, text_extracted_folder, results_folder, doctype
                )
                    return method, text_extracted, ocr_method
                except Exception as e:
                    print("Error: ", e)
                    continue
    else:
        print("file is not a pdf")
        process_images(file_path, image_preprocessed_folder)
        procesed_images_list = FileUtils.create_list(image_preprocessed_folder)
        process_image_files(
            procesed_images_list,
            image_preprocessed_folder,
            image_improved_folder,
            text_extracted_folder,
        )
        all_text_files = FileUtils.list_text_files(text_extracted_folder)
        for text_file in all_text_files:
            text_extracted, ocr_method, method = process_text_file(
                text_file, text_extracted_folder, results_folder, doctype
            )

            return method, text_extracted, ocr_method



# %% Main function
def main(file_path=str, doctype=str) -> dict:
    if doctype not in ["IMSS", "INFONAVIT", "SAT"]:
        raise ValueError(
            "Document type not recognized. please provide a document type: IMSS, ISSTE, SAT"
        )
    data = {"name" : "", "content": "", "entity_recognition": "", "ocr": "", "values": {}}
    data["name"] = os.path.basename(file_path)
    data["content"] = doctype
    if doctype == "IMSS":
        method, values, recognition = document_handler(file_path, doctype, "regex")
        data["values"] = values
        data["ocr"] = method
        data["entity_recognition"] = recognition
        FileUtils.save(results_folder + "/" + data["name"][:-3], json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True))
        
        """
        method, values, recognition = document_handler(file_path, doctype, "openai")
        data["values"] = values
        data["ocr"] = method
        data["entity_recognition"] = recognition
        FileUtils.save(results_folder + "/" + data["name"][:-3], json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True))
        """



    if doctype == "INFONAVIT":
        method, values, recognition = document_handler(file_path, doctype, "regex")
        data["values"] = values
        data["ocr"] = method
        data["entity_recognition"] = recognition
        FileUtils.save(results_folder + "/" + data["name"][:-3], json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True))

        """
        method, values, recognition = document_handler(file_path, doctype, "openai")
        data["values"] = values
        data["ocr"] = method
        data["entity_recognition"] = recognition
        FileUtils.save(results_folder + "/" + data["name"][:-3], json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True))
        """
        

    if doctype == "SAT":
        method, values, recognition = document_handler(file_path, doctype, "regex")
        data["values"] = values
        data["ocr"] = method
        data["entity_recognition"] = recognition
        FileUtils.save(results_folder + "/" + data["name"][:-3], json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True))

        """
        method, values, recognition = document_handler(file_path, doctype, "openai")
        data["values"] = values
        data["ocr"] = method
        data["entity_recognition"] = recognition
        FileUtils.save(results_folder + "/" + data["name"][:-3], json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True))
        """


    
    print(data)
    return data



# %% Run main function
if __name__ == "__main__":
    # Remove files for all output folders
    FileUtils.delete_from_folder(image_preprocessed_folder)
    FileUtils.delete_from_folder(image_improved_folder)
    FileUtils.delete_from_folder(text_extracted_folder)
    FileUtils.delete_from_folder(results_folder)

    # get the list of files unprocessed for IMSS
    raw_imss_list = FileUtils.create_list(os.path.join(image_raw_folder, "IMSS"))
    # get the file paths for every image inside imss folder
    imss_files_path = os.path.join(image_raw_folder, "IMSS")
    # get the original names of the files
    imss_original_names = FileUtils.get_original_names(imss_files_path)

    for file in raw_imss_list:
        file = os.path.join(imss_files_path, file)
        main(file, "IMSS")


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
