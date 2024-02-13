# %% google vision

from os import getcwd
from google.cloud import vision

folder_base_path = getcwd()

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
image_path = folder_base_path + "/1_image_preprocessed/0_procesed.jpeg"

# Send image to Google Vision API
texts = detect_text(image_path)

# Create one big text corpus
text_corpus = ""
for text in texts:
    text_corpus += f'\n"{text.description}"'

# Save as .txt
file_name = folder_base_path + "/3_text_extracted/0.txt"
with open(file_name, "w") as file:
    file.write(text_corpus)

# %%
