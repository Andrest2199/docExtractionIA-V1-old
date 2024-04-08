import os
from ono_ocr.utils import FileUtils
from ono_ocr.image_pre_procesing import (
    pdf_has_text,
    get_text_from_pdf,
    pdf_to_image,
    process_images,
)
from ono_ocr.improve_image_quality import improve_image_quality
from ono_ocr.ocr_aws_textract import extract_text_from_image


from django.conf import settings

base_dir = os.path.join(settings.BASE_DIR, "ono_ocr")
image_preprocessed_folder = os.path.join(base_dir, "1_image_preprocessed")
image_improved_folder = os.path.join(base_dir, "2_image_improved")


def document_handler(file_path=str, doctype=str):
    # Clean up folders
    FileUtils.delete_from_folder(image_preprocessed_folder)
    FileUtils.delete_from_folder(image_improved_folder)
    """
    This function is the main function that handles the document processing. It identifies the type of file and
    processes it accordingly.
    """
    file_name = os.path.basename(file_path)
    filetype = FileUtils.identify_file(file_name)

    if filetype == "pdf":
        """
        If the file is a PDF, check if it has text. If it does, extract the text and save it as a .txt file.
        """
        has_text = pdf_has_text(file_path)
        if has_text:
            text_corpus = get_text_from_pdf(file_path)
            return text_corpus

        images_list = pdf_to_image(file_path, image_preprocessed_folder)
    else:
        """
        If the file is an image, process it as an image.
        """
        images_list = process_images(file_path, image_preprocessed_folder)

    # iterate over document pages and improve image quality
    for image in images_list:
        image_path = os.path.join(image_preprocessed_folder, image)
        improve_image_quality(image_path, image_improved_folder)

    # create a list of improved images
    improved_images_list = FileUtils.create_list(image_improved_folder)

    # iterate over improved images and apply ocr
    for improved_image in improved_images_list:
        improved_image_path = os.path.join(image_improved_folder, improved_image)
        text_corpus = extract_text_from_image(improved_image_path)
        if len(improved_images_list) == 1:
            return text_corpus
        else:
            return [].append(text_corpus)
