# Object Character Recogniztion Tool for Grupo Ono

## Installation
Run the following command to install the required packages:
```bash
pip install -r requirements.txt
```
This will install all the required packages to run the OCR tool.
Also, you will need to install the dependencies managed by conda. To do so, run the following command:
```bash
conda install --file condarequirements.txt
```
If you have trouble installing the packages, you can try to install them manually by running the following commands:
```bash
conda install conda-forge::pypdf2
conda install anaconda::pillow
conda install numpy
pip install opencv-python
pip install deskew
```

You will also need to install the Google Cloud SDK. You can find the installation instructions [here](https://cloud.google.com/sdk/docs/install).
1) Install google CLI https://cloud.google.com/sdk/docs/install
2) Install google vision python library https://cloud.google.com/vision/docs/libraries
Additional documentation can be found [here](https://cloud.google.com/vision/docs/ocr).