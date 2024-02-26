# %% extract image from PDF

from PyPDF2 import PdfReader
from PIL import Image
import os
import shutil
import json
from utils.file_utils import FileUtils
import re

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


# output_folder_path = folder_base_path + "/1_image_preprocesed"
def identify_file(file: str) -> str:
    if file.endswith(".pdf"):
        return "pdf"
    elif file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
        return "image"
    else:
        return "other"


# Define function to check for pdf text
def pdf_has_text(file_path, string_threshold=10):
    # Extract text
    text_corpus = get_text_from_pdf(file_path)
    # Clean the text
    regex_cleaning_list = [r"\n", r"Escaneado con CamScanner"]
    for ii in range(len(regex_cleaning_list)):
        regex_pattern = regex_cleaning_list[ii]
        text_corpus = re.sub(regex_pattern, "", text_corpus)
    # If the length of the string is cero
    if len(text_corpus) > string_threshold:
        return True
    else:
        return False


def get_images_from_pdf(file_path=str, output_folder_path=str):
    file_name_procesed = os.path.basename(file_path).strip(".pdf") + "_procesed"
    # Create image file path input
    # Initialize a PdfReader object
    reader = PdfReader(file_path)
    # Loop through PDF pages
    for jj in range(len(reader.pages)):
        print("Page:", jj)
        page = reader.pages[jj]
        # Method 1 / following documentation
        if hasattr(page, "images") and page.images != []:
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
                FileUtils.save(file_path_output, image_file_object.data)
                print("Saved file:", file_name_procesed_pdf, "at ", file_path_output)

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
                        file_ext = (
                            "jpeg"  # Generic extension for unknown or unhandled types
                        )
                    file_name_procesed_pdf = (
                        f"{file_name_procesed}_{jj}_"
                        + f"{image_count}_{key[1:]}."
                        + file_ext
                    )
                    file_path_output = os.path.join(
                        output_folder_path, file_name_procesed_pdf
                    )
                    # Save the image in the output folder
                    FileUtils.save(file_path_output, image_data)
                    image_count += 1
                    print(
                        "Saved file:", file_name_procesed_pdf, "at ", file_path_output
                    )


def process_images(file_path, output_folder_path) -> None:
    """
    Function to process images"""
    filename = os.path.basename(file_path)
    file_name_procesed = f"{os.path.basename(file_path)}_procesed"
    # Logic for the rest of the images
    # Create image file path input
    # file_path_input = os.path.join(file_path, filename)
    # Create new image name
    with Image.open(file_path) as img:
        image_format = img.format
        image_format = image_format.lower()
    file_name_procesed_image = file_name_procesed + "." + image_format
    # Build the full source and target paths
    target_path = os.path.join(output_folder_path, file_name_procesed_image)
    # Copy the image to the target folder with the new name
    shutil.copy2(file_path, target_path)
    print("Saved file:", file_name_procesed_image)


# Define function to extract text
def get_text_from_pdf(file_path=str) -> str:
    """
    Function to extract text from a PDF file"""
    # Initialize a PDF reader object and read the PDF
    reader = PdfReader(file_path)

    # Initialize an empty string to hold all the text
    text_corpus = ""

    # Iterate through each page in the PDF and extract text
    for page in reader.pages:
        text_corpus += page.extract_text() + "\n"  # Adding a newline character

    return text_corpus


# %% extract text from PDFs
# Set folder paths
# input_folder_path = folder_base_path + "/SAT"
# output_folder_path = folder_base_path + "/3_text_extracted"

# # Set file path
# file_name = "CSF 1230673 RAMOS RODRIGUEZ VICTOR RAMON.pdf"  # "40 CSF ELIZABETH HERNANDEZ.pdf" #'CSF 1230673 RAMOS RODRIGUEZ VICTOR RAMON.pdf'
# input_file_path = os.path.join(input_folder_path, file_name)


# # Extract text
# text_corpus = extract_text(input_file_path)

# # Save text as txt in output folder path
# new_file_name = input_file_path.split("/")[-1].strip(".pdf") + ".txt"
# new_file_name = file_name.strip(".pdf") + ".txt"
# file_path_output = os.path.join(output_folder_path, new_file_name)
# with open(file_path_output, "w") as file:
#     file.write(text_corpus)


# text_in_pdf = pdf_has_text(input_file_path)


# %%
