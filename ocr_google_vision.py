# %% google vision

import os
from google.cloud import vision


folder_base_path = os.getcwd()

"""
SET-UP
1) Install google CLI https://cloud.google.com/sdk/docs/install
2) Install google vision python library https://cloud.google.com/vision/docs/libraries

DOCS:
https://cloud.google.com/vision/docs/ocr

TODO:
1) Run function to detect handwriting in images 
2) Run function to detect text in PDF files
3) Compare results between three OCR methods
"""

# %% Set up folder paths

# Set folder paths
# input_folder_path = folder_base_path + "/1_image_preprocessed/"
# output_folder_path = folder_base_path + "/3_text_extracted/"

# %% Quick start


def run_quickstart() -> vision.EntityAnnotation:
    """Provides a quick start example for Cloud Vision."""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The URI of the image file to annotate
    file_uri = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"

    image = vision.Image()
    image.source.image_uri = file_uri

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print("Labels:")
    for label in labels:
        print(label.description)

    return labels


# %% Detect text in images in local directory
# https://cloud.google.com/vision/docs/ocr


# Define function to detect text in the image file
def detect_text(path):

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")

    for text in texts:
        print(f'\n"{text.description}"')

        vertices = [
            f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        ]

        print("bounds: {}".format(",".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return texts


# Specify path to image
# image_path = folder_base_path + "/1_image_preprocessed/5_procesed_0_0_Image9.jpg"

# # Send image to Google Vision API
# texts = detect_text(image_path)

# # Create one big text corpus
# text_corpus = ""
# for text in texts:
#     text_corpus += f'\n"{text.description}"'

# # Save as .txt
# file_name = folder_base_path + "/3_text_extracted/0.txt"
# with open(file_name, "w") as file:
#     file.write(text_corpus)

# %% Detect handwriting in local images
# https://cloud.google.com/vision/docs/handwriting


def detect_handwriting(path):

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    text_corpus = ""
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print(f"\nBlock confidence: {block.confidence}\n")

            for paragraph in block.paragraphs:
                print("Paragraph confidence: {}".format(paragraph.confidence))

                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])
                    print(
                        "Word text: {} (confidence: {})".format(
                            word_text, word.confidence
                        )
                    )
                    # TODO Change to | instead of \n
                    text_corpus = "\n".join([text_corpus, word_text])

                    for symbol in word.symbols:
                        print(
                            "\tSymbol: {} (confidence: {})".format(
                                symbol.text, symbol.confidence
                            )
                        )

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return text_corpus


def ocr_google_vision(image_path, output_folder_path):
    print(f"Running Google Vision API for {image_path}")
    # TODO separate logic for handwriting and text printed, separate for | every word
    """ " Function to run the Google Vision API to detect handwriting and text in images
    Args:
    image_path: str, path to the image
    output_folder_path: str, path to the output folder
    """
    text_corpus = detect_handwriting(image_path)
    file_name = os.path.basename(image_path).split(".")[0] + "_HW.txt"
    file_path_output_hw = os.path.join(output_folder_path, file_name)
    with open(file_path_output_hw, "w") as file:
        file.write(text_corpus)
    texts = detect_text(image_path)
    text_corpus = ""
    for text in texts:
        text_corpus += f'\n"{text.description}"'
    file_name = os.path.basename(image_path).split(".")[0] + "_text_PT.txt"
    file_path_output_pt = os.path.join(output_folder_path, file_name)
    with open(file_path_output_pt, "w") as file:
        file.write(text_corpus)


# Specify path to image
# image_name = "5_procesed_0_0_Image9.jpg"
# image_path = os.path.join(input_folder_path, image_name)

# # Send image to Google Vision API
# text_corpus = detect_handwriting(image_path)

# # Save as .txt
# file_name = "5_text.txt"
# file_path_output = os.path.join(output_folder_path, file_name)

# with open(file_path_output, "w") as file:
#     file.write(text_corpus)

# %%
