import os
from ono_ocr.models import Extraction

cwd = os.getcwd()
image_raw_folder = os.path.join(cwd, "0_image_raw")
image_preprocessed_folder = os.path.join(cwd, "1_image_preprocessed")
image_improved_folder = os.path.join(cwd, "2_image_improved")
text_extracted_folder = os.path.join(cwd, "3_text_extracted")
results_folder = os.path.join(cwd, "4_results")
data_inject_folder = os.path.join(cwd, "data_inject")


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
    #     FileUtils.delete_from_folder(text_extracted_folder)

    extraction = Extraction(
        doctype=doctype,
        original_filename=os.path.basename(file_path),
        ocr="openai_vision",
        entity_recognition="chat_completions",
        values={"value1": "value1", "value2": "value2"},
        raw_text="raw_text_asdasdasd",
    )
    data = extraction.to_json()

    return data

    # methods = ["openai", "google", "aws_textract", "aws_parser"]
    # for method in methods:
    #     ocr = document_handler(file_path, doctype, method)
    #     all_text_files = FileUtils.list_text_files(text_extracted_folder)

    #     for text_file in all_text_files:
    #         print("text file", text_file)
    #         if text_file.endswith(".txt"):
    #             entity_methods = [
    #                 "txt_extraction",
    #                 "chat_completions",
    #             ]

    #             for entity_method in entity_methods:
    #                 raw_text, values, recognition = process_text_file(
    #                     text_file, doctype, entity_method
    #                 )
    #                 data["plain text"] = Utils.decode_text(raw_text)
    #                 data["values"] = Utils.decode_text(values)
    #                 data["ocr"] = ocr
    #                 data["entity_recognition"] = recognition

    #                 data = Extraction.to_json(
    #                     doctype=doctype,
    #                     original_filename=os.path.basename(file_path),
    #                     ocr="openai_vision",
    #                     entity_recognition="chat_completions",
    #                     values={"value1": "value1", "value2": "value2"},
    #                     raw_text="raw_text_asdasdasd",
    #                 )

    #                 FileUtils.save(
    #                     f"{results_folder}/{data['name'][:-4]}_{data['ocr']}_{data['entity_recognition']}.json",
    #                     json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True),
    #                 )
    #         elif text_file.endswith(".json"):
    #             entity_methods = [
    #                 "json_extraction",
    #                 "chat_completions",
    #             ]
    #             for entity_method in entity_methods:
    #                 raw_text, values, recognition = process_text_file(
    #                     text_file, doctype, entity_method
    #                 )
    #                 data["plain text"] = Utils.decode_text(raw_text)
    #                 data["values"] = Utils.decode_text(values)
    #                 data["ocr"] = ocr
    #                 data["entity_recognition"] = recognition
    #                 FileUtils.save(
    #                     f"{results_folder}/{data['name'][:-4]}_{data['ocr']}_{data['entity_recognition']}.json",
    #                     json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True),
    #                 )
    #     # TODO: call process to get system_accuracy forloop
    # return data
