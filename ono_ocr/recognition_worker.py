import os
from ono_ocr.models import Extraction
from ono_ocr.utils import FileUtils
from ono_ocr.document_handler import document_handler
from ono_ocr.entity_recognition import chat_completions_entity_extraction
from django.conf import settings

base_dir = os.path.join(settings.BASE_DIR, "ono_ocr")

image_raw_folder = os.path.join(base_dir, "0_image_raw")
image_preprocessed_folder = os.path.join(base_dir, "1_image_preprocessed")
# image_improved_folder = os.path.join(base_dir, "2_image_improved")
# text_extracted_folder = os.path.join(base_dir, "3_text_extracted")
# results_folder = os.path.join(base_dir, "4_results")
data_inject_folder = os.path.join(base_dir, "data_inject")

# TODO: Add logic for two paged documents
# TODO: return instructions in the api (system_role and user content)


def recognition_worker(file_path=str, doctype=str) -> dict:
    """
    Main function to process the document and extract the information from it.
    Args:
        file_path: Path to the document to process.
        doctype: Type of document to process. It can be one of the following: IMSS, INFONAVIT, SAT.
    Returns:
        dict: A dictionary with the extracted information from the document.
    """

    if doctype not in ["IMSS", "INFONAVIT", "SAT"]:
        raise ValueError(
            "Document type not recognized. Please provide a valid document type: IMSS, INFONAVIT, SAT"
        )
    # FileUtils.delete_from_folder(text_extracted_folder)
    FileUtils.delete_from_folder(image_raw_folder)

    # copy file to image_raw_folder
    file_path = FileUtils.copy_file(file_path, image_raw_folder)

    text_extracted = document_handler(file_path, doctype)

    fields_extracted = chat_completions_entity_extraction(
        text_extracted, data_inject_folder, doctype
    )

    extraction = Extraction(
        doctype=doctype,
        original_filename=os.path.basename(file_path),
        # ocr="openai_vision",
        entity_recognition="chat_completions",
        values=fields_extracted,
        raw_text=text_extracted,
    )

    return extraction.to_json()
