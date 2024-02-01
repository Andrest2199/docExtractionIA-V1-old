# %% extract image from PDF

from PyPDF2 import PdfReader
from PIL import Image
import os
import shutil

folder_base_path = os.getcwd()

"""
INSTALLATION:
conda install conda-forge::pypdf2
conda install anaconda::pillow

TODO's:
- Debug why certain pdfs are not saved
- Save data as json

POTENTIAL IMPROVEMENTS
- Using regex extract employee name and number
"""

# %%

# Set folder paths
input_folder_path = folder_base_path + '/0_data_original'
output_folder_path = folder_base_path +  '/1_data_procesed'

# Create file name list
file_name_list = []
for file_name_original in os.listdir(input_folder_path):
    # Remove non-ASCII characters 
    file_name_original_clean = file_name_original.encode('ascii', errors='ignore').decode()
    # Append original file name cleaned
    file_name_list.append(file_name_original_clean)

# Create data dictionary and extract original file name
data = {}
for ii in range(len(file_name_list)):
    file_name_original = file_name_list[ii]
    data[ii] = {'file_name_original': file_name_original}

# Loop through all the files in the input folder
file_number = 0
for file_name_original in os.listdir(input_folder_path):
    file_name_procesed = f'{file_number}_procesed'

    # Logic for PDFs    
    if file_name_original.endswith(".pdf"):
        # Create image file path input
        file_path_input = os.path.join(input_folder_path, file_name_original)
        # Initialize a PdfReader object
        reader = PdfReader(file_path_input)
        # Loop through PDF pages
        for jj in range(len(reader.pages)):
            page = reader.pages[jj]
            image_count = 0
            # Loop through images in each PDF page
            for image_file_object in page.images:
                # Create image file path output
                file_name_procesed_pdf = f'{file_name_procesed}_{jj}_{image_file_object.name}'
                file_path_output = output_folder_path + '/' + file_name_procesed_pdf
                # Save the image in the output folder
                with open(file_path_output, "wb") as fp: 
                    fp.write(image_file_object.data)
                    image_count += 1
                    print("Saved file:", file_name_procesed_pdf)
   
    # Logic for the rest of the images
    elif not file_name_original.endswith(".pdf"):
        # Create image file path input
        file_path_input = os.path.join(input_folder_path, file_name_original)
        # Create new image name
        with Image.open(file_path_input) as img:
            image_format = img.format
            image_format = image_format.lower()
        file_name_procesed_image = file_name_procesed + '.' + image_format 

        # Build the full source and target paths
        source_path = os.path.join(input_folder_path, file_name_original)
        target_path = os.path.join(output_folder_path, file_name_procesed_image)
        # Copy the image to the target folder with the new name
        shutil.copy2(source_path, target_path)
        print("Saved file:", file_name_procesed_image)
    
    # Increase the file number
    file_number += 1

# %% Extract images from pdf

reader = PdfReader(folder_base_path + '/0_data_original/261207 DAGNINO ROMO CARLOS ALFREDO UP 726741.pdf')

page = reader.pages[0]
count = 0

for image_file_object in page.images:
    with open(folder_base_path + '/1_data_procesed/' + str(count) + image_file_object.name, "wb") as fp: 
        fp.write(image_file_object.data)
        count += 1

# %%