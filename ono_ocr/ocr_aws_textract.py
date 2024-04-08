# %% ocr_aws_textract

import time
import os
import boto3
from PIL import Image, ImageDraw

from trp import Document


"""
# Code samples https://github.com/aws-samples/amazon-textract-code-samples

# Libraries:
Install boto3
pip install amazon-textract-response-parser
"""

# %% Detect text in images

# Specify path to image
# documentName = folder_base_path + "/0_image_raw/7_procesed.jpg"

# # Read document content
# with open(documentName, "rb") as document:
#     imageBytes = bytearray(document.read())

# Amazon Textract client
textract = boto3.client("textract")

# Call Amazon Textract
# response = textract.detect_document_text(Document={"Bytes": imageBytes})

# print(response)

# Print detected text
# for item in response["Blocks"]:
#     if item["BlockType"] == "LINE":
#         print("\033[94m" + item["Text"] + "\033[0m")

# %%  Extract text in PDFs


def start_job(client, s3_bucket_name, object_name):
    response = None
    response = client.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": s3_bucket_name, "Name": object_name}}
    )

    return response["JobId"]


def is_job_complete(client, job_id):
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while status == "IN_PROGRESS":
        time.sleep(1)
        response = client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status


def get_job_results(client, job_id):
    pages = []
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    pages.append(response)
    print("Resultset page received: {}".format(len(pages)))
    next_token = None
    if "NextToken" in response:
        next_token = response["NextToken"]

    while next_token:
        time.sleep(1)
        response = client.get_document_text_detection(
            JobId=job_id, NextToken=next_token
        )
        pages.append(response)
        print("Resultset page received: {}".format(len(pages)))
        next_token = None
        if "NextToken" in response:
            next_token = response["NextToken"]

    return pages


""""
if __name__ == "__main__":
    # Document
    s3_bucket_name = "ki-textract-demo-docs"
    document_name = "Amazon-Textract-Pdf.pdf"
    region = "us-east-1"
    client = boto3.client("textract", region_name=region)

    job_id = start_job(client, s3_bucket_name, document_name)
    print("Started job with id: {}".format(job_id))
    if is_job_complete(client, job_id):
        response = get_job_results(client, job_id)

    # print(response)

    # Print detected text
    for result_page in response:
        for item in result_page["Blocks"]:
            if item["BlockType"] == "LINE":
                print("\033[94m" + item["Text"] + "\033[0m")

"""
# %% Forms
""""
# Document
documentName = (
    folder_base_path + "/0_image_raw/7_procesed.jpg"
)

# Amazon Textract client
textract = boto3.client("textract")

# Call Amazon Textract
with open(documentName, "rb") as document:
    response = textract.analyze_document(
        Document={
            "Bytes": document.read(),
        },
        FeatureTypes=["FORMS"],
    )

# print(response)
"""
""""
doc = Document(response)

for page in doc.pages:
    # Print fields
    print("Fields:")
    for field in page.form.fields:
        print("Key: {}, Value: {}".format(field.key, field.value))

    # Get field by key
    print("\nGet Field by Key:")
    key = "Phone Number:"
    field = page.form.getFieldByKey(key)
    if field:
        print("Key: {}, Value: {}".format(field.key, field.value))

    # Search fields by key
    print("\nSearch Fields:")
    key = "address"
    fields = page.form.searchFieldsByKey(key)
    for field in fields:
        print("Key: {}, Value: {}".format(field.key, field.value))

"""
# TODO: Create and return a dictionary with the fields and values


# %% Forms redaction
""""
import boto3
from trp import Document
from PIL import Image, ImageDraw

# Document
documentName = "employmentapp.png"

# Amazon Textract client
textract = boto3.client("textract")

# Call Amazon Textract
with open(documentName, "rb") as document:
    response = textract.analyze_document(
        Document={
            "Bytes": document.read(),
        },
        FeatureTypes=["FORMS"],
    )

# print(response)

doc = Document(response)

# Redact document
img = Image.open(documentName)

width, height = img.size

if doc.pages:
    page = doc.pages[0]
    for field in page.form.fields:
        if field.key and field.value and "address" in field.key.text.lower():
            # if(field.key and field.value):
            print(
                "Redacting => Key: {}, Value: {}".format(
                    field.key.text, field.value.text
                )
            )

            x1 = field.value.geometry.boundingBox.left * width
            y1 = field.value.geometry.boundingBox.top * height - 2
            x2 = x1 + (field.value.geometry.boundingBox.width * width) + 5
            y2 = y1 + (field.value.geometry.boundingBox.height * height) + 2

            draw = ImageDraw.Draw(img)
            draw.rectangle([x1, y1, x2, y2], fill="Black")

img.save("redacted-{}".format(documentName))
"""

# %% Extract text and create dictionary
# TODO: call from main function
# Document
# image_path = (
#     folder_base_path + "/0_image_raw/695844 MACIAS LARA JORGE ARMANDO MI909883 ok.jpeg"
# )


# Create function to extract text corpus and identify fields in forms
def extract_text_from_image(image_path: str) -> str:
    print("Extracting text from image with AWS...")
    # Amazon Textract client
    textract = boto3.client("textract")

    # Read document content
    with open(image_path, "rb") as document:
        imageBytes = bytearray(document.read())

    # Call Amazon Textract
    response = textract.detect_document_text(Document={"Bytes": imageBytes})

    # Create text corpus
    text_corpus = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text_corpus += item["Text"] + " "

    return text_corpus


# Analyze document and create dictionary with fields
def anlyse_text_and_create_dict(image_path: str) -> dict:
    print("Analyzing text and creating dictionary with AWS...")

    # Call Amazon Textract / analyze document
    with open(image_path, "rb") as document:
        response = textract.analyze_document(
            Document={
                "Bytes": document.read(),
            },
            FeatureTypes=["FORMS"],
        )

    # Parse response into document with awz-textract-response-parser
    doc = Document(response)

    # Create new empty dictionary
    fields_dict = {}

    # Iterate over each page in the document
    for page in doc.pages:
        print("Fields:")
        # Iterate over each field in the form on the page
        for field in page.form.fields:
            # Print the key and value of the field
            print("Key: {}, Value: {}".format(field.key, field.value))
            # If both the key and value of the field exist
            if field.key and field.value:
                # Add the text of the key and value to the fields_dict dictionary
                fields_dict[field.key.text] = field.value.text
            # If only the key of the field exists
            elif field.key:
                # Add the text of the key to the fields_dict dictionary with a value of None
                fields_dict[field.key.text] = None

        return fields_dict


# %%
