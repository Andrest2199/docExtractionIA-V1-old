import numpy as np
import os

from ono_ocr.utils.file_utils import FileUtils

# Global variables
IMSS_MEAN_LENGTH = None
IMSS_STD_LENGTH = None
INFONAVIT_MEAN_LENGTH = None
INFONAVIT_STD_LENGTH = None
SAT_MEAN_LENGTH = None
SAT_STD_LENGTH = None


def length_threshold_calculator(data_inject_folder):
    """
    This function validates the raw text extracted from the documents. Sets the global variables for the mean and
    standard deviation of the text length for each document type.
    """

    global IMSS_MEAN_LENGTH, IMSS_STD_LENGTH
    global INFONAVIT_MEAN_LENGTH, INFONAVIT_STD_LENGTH
    global SAT_MEAN_LENGTH, SAT_STD_LENGTH

    imss_data_inject_sub_folder = os.path.join(data_inject_folder, "IMSS")
    infonavit_data_inject_sub_folder = os.path.join(data_inject_folder, "INFONAVIT")
    sat_data_inject_sub_folder = os.path.join(data_inject_folder, "SAT")

    IMSS_MEAN_LENGTH, IMSS_STD_LENGTH = process_files(imss_data_inject_sub_folder, [], [])
    INFONAVIT_MEAN_LENGTH, INFONAVIT_STD_LENGTH = process_files(infonavit_data_inject_sub_folder, [], [])
    SAT_MEAN_LENGTH, SAT_STD_LENGTH = process_files(sat_data_inject_sub_folder, [], [])

    return {
        "IMSS": {"mean_length": IMSS_MEAN_LENGTH, "std_length": IMSS_STD_LENGTH},
        "INFONAVIT": {"mean_length": INFONAVIT_MEAN_LENGTH, "std_length": INFONAVIT_STD_LENGTH},
        "SAT": {"mean_length": SAT_MEAN_LENGTH, "std_length": SAT_STD_LENGTH},
    }


def process_files(data_inject_sub_folder, result_txt_list, input_txt_list):
    """
    This function processes the files in the data inject folder.
    returns the mean and standard deviation of the text length.
    """
    data_inject_files = FileUtils.get_paths(data_inject_sub_folder, 2)
    txt_count = 0
    for file in data_inject_files:
        filename = os.path.basename(file)
        if filename.startswith("result"):
            result_txt_list.append(FileUtils.read(file))
        elif filename.startswith("data"):
            input_txt_list.append(FileUtils.read(file))
        else:
            print(f"File {file} not recognized")
        txt_count += 1
    print(f"Processed {txt_count} files")
    lengths = [len(text) for text in input_txt_list]
    mean_length = np.mean(lengths)
    std_length = np.std(lengths)

    return mean_length, std_length


