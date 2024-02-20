# %% extract image from PDF

from PyPDF2 import PdfReader
from PIL import Image
import os
import shutil
import json
import utils

folder_base_path = os.getcwd()

"""
INSTALLATION:
conda install conda-forge::pypdf2
conda install anaconda::pillow

TODO's:
- Delete, escaneado from scanscanner
- In a 2nd version explore other libriares to extract images from PDFs

POTENTIAL IMPROVEMENTS
- Using regex extract employee name, folio ID and employee ID. Andres to ask Adriana de la Rosa.
"""

# %%


# Set folder paths
# input_folder_path = folder_base_path + "/0_image_raw"
# output_folder_path = folder_base_path + "/1_image_procesed"


def process_images(input_folder_path, output_folder_path):
    # Delete all files in output folder path


    # Create file name list
    file_name_list = utils.create_file_list(input_folder_path)

    # Create data dictionary and extract original file name
    data = {}
    for ii in range(len(file_name_list)):
        file_name_original = file_name_list[ii]
        if file_name_original != ".gitignore" and file_name_original != ".DS_Store":
            data[ii] = {"file_name_original": file_name_original}

    # Loop through all the files in the input folder
    file_number = 0
    for file_name_original in os.listdir(input_folder_path):
        file_name_procesed = f"{file_number}_procesed"

        # Logic for PDFs
        if file_name_original.endswith(".pdf"):
            # Create image file path input
            file_path_input = os.path.join(input_folder_path, file_name_original)
            # Initialize a PdfReader object
            reader = PdfReader(file_path_input)
            # Loop through PDF pages
            for jj in range(len(reader.pages)):
                page = reader.pages[jj]
                # Method 1 / following documentation
                if hasattr(page, "images") and page.images != []:
                    image_count = 0
                    # Loop through images in each PDF page
                    for image_file_object in page.images:
                        # Create image file path output
                        file_name_procesed_pdf = (
                            f"{file_name_procesed}_{jj}_{image_file_object.name}"
                        )
                        file_path_output = (
                            output_folder_path + "/" + file_name_procesed_pdf
                        )  # TODO: Use os.path.join()
                        # Save the image in the output folder
                        with open(file_path_output, "wb") as fp:
                            fp.write(image_file_object.data)
                        image_count += 1
                        print("Saved file:", file_name_procesed_pdf)

                # Method 2 / check pdf structure
                else:
                    image_count = 0
                    # Get xobject subtype Image
                    resources = page.get("/Resources").getObject()
                    xobjects = resources["/XObject"] if resources else {}
                    for key, obj in xobjects.items():
                        xobject = obj.get_object()
                        # Logic to check for images
                        if xobject["/Subtype"] == "/Image":
                            image_data = xobject.get_data()
                            image_filter = xobject.get("/Filter")
                            # Determine the correct file extension
                            if image_filter == "/DCTDecode":
                                file_ext = "jpg"
                            elif image_filter == "/JPXDecode":
                                file_ext = "jp2"
                            elif image_filter == "/FlateDecode":
                                # Simplified assumption for PNG, might not be accurate for all cases
                                file_ext = "png"
                            else:
                                # Simplified assumption for jpeg, might not be accurate for all cases
                                file_ext = "jpeg"  # Generic extension for unknown or unhandled types
                            file_name_procesed_pdf = (
                                f"{file_name_procesed}_{jj}_"
                                + f"{image_count}_{key[1:]}."
                                + file_ext
                            )
                            file_path_output = os.path.join(
                                output_folder_path, file_name_procesed_pdf
                            )
                            # Save the image in the output folder
                            with open(file_path_output, "wb") as image_file:
                                image_file.write(image_data)
                            image_count += 1
                            print("Saved file:", file_name_procesed_pdf)

        # Logic for the rest of the images
        elif (
            not file_name_original.endswith(".pdf")
            and file_name_original != ".gitignore"
            and file_name_original != ".DS_Store"
        ):
            # Create image file path input
            file_path_input = os.path.join(input_folder_path, file_name_original)
            # Create new image name
            with Image.open(file_path_input) as img:
                image_format = img.format
                image_format = image_format.lower()
            file_name_procesed_image = file_name_procesed + "." + image_format

            # Build the full source and target paths
            source_path = os.path.join(input_folder_path, file_name_original)
            target_path = os.path.join(output_folder_path, file_name_procesed_image)
            # Copy the image to the target folder with the new name
            shutil.copy2(source_path, target_path)
            print("Saved file:", file_name_procesed_image)

        # Increase the file number
        file_number += 1
        # %% Save data as json
        file_name = output_folder_path + "/data.json"
        with open(file_name, "w") as json_file:
            json.dump(data, json_file, indent=4)


# %%
