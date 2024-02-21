# %% extract image from PDF

from PyPDF2 import PdfReader
from PIL import Image
import os
import shutil
import json
import utils
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


# Set folder paths
# input_folder_path = folder_base_path + "/0_image_raw"
# output_folder_path = folder_base_path + "/1_image_preprocesed"


def process_images(input_folder_path, output_folder_path):

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


# %% extract text from PDFs

# Set folder paths
input_folder_path = folder_base_path + '/SAT'
output_folder_path = folder_base_path + '/3_text_extracted'

# Set file path
file_name = 'CSF 1230673 RAMOS RODRIGUEZ VICTOR RAMON.pdf' #"40 CSF ELIZABETH HERNANDEZ.pdf" #'CSF 1230673 RAMOS RODRIGUEZ VICTOR RAMON.pdf'
input_file_path = os.path.join(input_folder_path, file_name) 

# Define function to extract text
def extract_text(input_file_path):
    # Initialize a PDF reader object and read the PDF
    reader = PdfReader(input_file_path)

    # Initialize an empty string to hold all the text
    text_corpus = ""

    # Iterate through each page in the PDF and extract text
    for page in reader.pages:
        text_corpus += page.extract_text() + "\n"  # Adding a newline character

    return text_corpus

# Extract text
text_corpus = extract_text(input_file_path)

# Save text as txt in output folder path
new_file_name = input_file_path.split('/')[-1].strip('.pdf') + '.txt'
new_file_name = file_name.strip('.pdf') + '.txt'
file_path_output = os.path.join(output_folder_path, new_file_name)
with open(file_path_output, "w") as file:
    file.write(text_corpus)

# Define function to check for pdf text
def pdf_has_text(input_file_path, string_threshold=10):
    # Extract text
    text_corpus = extract_text(input_file_path)
    # Clean the text
    regex_cleaning_list = [r'\n', r'Escaneado con CamScanner']
    for ii in range(len(regex_cleaning_list)):
        regex_pattern = regex_cleaning_list[ii]
        text_corpus = re.sub(regex_pattern, '', text_corpus)
    # If the length of the string is cero
    if len(text_corpus) > string_threshold:
        return True
    else:
        return False

text_in_pdf = pdf_has_text(input_file_path)

# %%
