# %% Import libraries
import json
from image_pre_procesing import process_images
from improve_image_quality import improve_image_quality
from ocr_openai_vision import ocr_openai_vision
from ocr_google_vision import ocr_google_vision
from cleaning_extract_process import data_cleaning, data_extraction, regex_extraction
import os
import utils
import os

# %% Set the paths
folder_base_path = os.getcwd()
image_raw_folder = os.path.join(folder_base_path, "0_image_raw")
image_preprocessed_folder = os.path.join(folder_base_path, "1_image_preprocessed")
image_improved_folder = os.path.join(folder_base_path, "2_image_improved")
text_extracted_folder = os.path.join(folder_base_path, "3_text_extracted")
results_folder = os.path.join(folder_base_path, "4_results")


# %% Main function
def main():
    # Process images
    process_images(image_raw_folder, image_preprocessed_folder)
    #  %% improves image quality
    all_images = utils.create_file_list(image_preprocessed_folder)
    for image in all_images:
        improve_image_quality(
            image_preprocessed_folder + "/" + image,
            image_improved_folder + "/" + image,
        )
    # %% get improved images
    improved_images = utils.create_file_list(image_improved_folder)
    #  %% ocr openai vision
    for image in improved_images:
        ocr_openai_vision(image_improved_folder + "/" + image, text_extracted_folder)

    # %% ocr_google_vision
    for image in improved_images:
        ocr_google_vision(image_improved_folder + "/" + image, text_extracted_folder)

    # %% Extract data
    all_text_files = utils.list_text_files(text_extracted_folder)
    for text_file in all_text_files:
        data_retrieval(
            text_extracted_folder + "/" + text_file,
            results_folder,
        )


# %% Run main function
if __name__ == "__main__":
    main()

# %%
