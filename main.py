# %% Import libraries
from image_pre_procesing import process_images
from improve_image_quality import improve_image_quality
import os
import utils

# %% Set the paths
folder_base_path = os.getcwd()
image_raw_folder = folder_base_path + "/0_image_raw"
image_preprocessed_folder = folder_base_path + "/1_image_preprocessed"
image_improved_folder = folder_base_path + "/2_image_improved"


# %% Main function
def main():
    # Process images
    process_images(image_raw_folder, image_preprocessed_folder)
    # Get all file paths in a folder
    all_images = utils.create_file_list(image_preprocessed_folder)
    print(f"Images to process: {all_images}")
    for image in all_images:
        image_processed = improve_image_quality(
            image_preprocessed_folder + "/" + image,
            image_improved_folder + "/" + image,
        )
        print(f"Image {image} processed: {image_processed}")


if __name__ == "__main__":
    main()

# %%
