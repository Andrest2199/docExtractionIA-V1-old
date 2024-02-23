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
import os
from file_utils import FileUtils
import os

# %% Set the paths

folder_base_path = os.getcwd()
image_raw_folder = os.path.join(folder_base_path, "0_image_raw")
image_preprocessed_folder = os.path.join(folder_base_path, "1_image_preprocessed")
image_improved_folder = os.path.join(folder_base_path, "2_image_improved")
text_extracted_folder = os.path.join(folder_base_path, "3_text_extracted")
results_folder = os.path.join(folder_base_path, "4_results")


# %% Main function
def main(file_path=str, doctype=str) -> dict:
    if doctype not in ["IMSS", "ISSTE", "SAT"]:
        raise ValueError(
            "Document type not recognized. please provide a document type: IMSS, ISSTE, SAT"
        )
    if doctype == "IMSS":
        file_name = os.path.basename(file_path)
        filetype = identify_file(file_name)
        if filetype == "pdf":
            has_text = pdf_has_text(file_path)
            if has_text:
                print("file has text inside")
                text_corpus = get_text_from_pdf(file_path)
                new_file_name = file_name.strip(".pdf") + ".txt"
                FileUtils.save(text_extracted_folder + "/" + new_file_name, text_corpus)
                text_extracted = FileUtils.read(
                    text_extracted_folder + "/" + new_file_name
                )
                result = regex_extraction(text_extracted)
                json_str = json.dumps(
                    result, ensure_ascii=True, indent=2, sort_keys=True
                )
                FileUtils.save(results_folder + "/" + file_name, json_str)
            else:
                print("file does not have text inside")
                get_images_from_pdf(file_path, image_preprocessed_folder)
                # improve images
                procesed_images_list = FileUtils.create_list(image_preprocessed_folder)
                for image in procesed_images_list:
                    images_path = os.path.join(image_preprocessed_folder, image)
                    # improve image quality
                    improve_image_quality(
                        images_path, os.path.join(image_improved_folder, image)
                    )
                improved_images_list = FileUtils.create_list(image_improved_folder)
                for image in improved_images_list:

                    # apply ocr openai vision
                    images_path = os.path.join(image_preprocessed_folder, image)

                    ocr_openai_vision(
                        images_path,
                        text_extracted_folder,
                    )
                    # apply ocr google vision
                    ocr_google_vision(images_path, text_extracted_folder)
                all_text_files = FileUtils.list_text_files(text_extracted_folder)
                for text_file in all_text_files:
                    text_file_path = os.path.join(text_extracted_folder, text_file)
                    if text_file.endswith(".txt"):
                        json_str = FileUtils.read(text_file_path)
                        extracted_text = regex_extraction(json_str)
                        json_str = json.dumps(
                            extracted_text,
                            ensure_ascii=True,
                            indent=2,
                            sort_keys=True,
                        )
                        FileUtils.save(results_folder + "/" + text_file, json_str)
                    elif text_file.endswith(".json"):
                        data_cleaned = data_cleaning(text_file)
                        extracted_text = data_extraction(data_cleaned, "incapacidades")

        else:
            print("file is not a pdf")
            process_images(file_path, image_preprocessed_folder)
            procesed_images_list = FileUtils.create_list(image_preprocessed_folder)
            for image in procesed_images_list:
                images_path = os.path.join(image_preprocessed_folder, image)

                # improve image quality
                improve_image_quality(
                    images_path, os.path.join(image_improved_folder, image)
                )
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
            all_text_files = FileUtils.list_text_files(text_extracted_folder)
            for text_file in all_text_files:
                text_file_path = os.path.join(text_extracted_folder, text_file)
                if text_file.endswith(".txt"):
                    json_str = FileUtils.read(text_file_path)
                    extracted_text = regex_extraction(json_str)
                    json_str = json.dumps(
                        extracted_text,
                        ensure_ascii=True,
                        indent=2,
                        sort_keys=True,
                    )
                    FileUtils.save(results_folder + "/" + text_file, json_str)
                elif text_file.endswith(".json"):
                    data_cleaned = data_cleaning(text_file)
                    extracted_text = data_extraction(data_cleaned, "incapacidades")


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
    # save the original names of the files
    # FileUtils.save(
    #     os.path.join(image_preprocessed_folder, "imss_original_filenames.json"),
    #     json.dumps(imss_original_names),
    # )
    for file in raw_imss_list:
        file = os.path.join(imss_files_path, file)
        main(file, "IMSS")

# %%
