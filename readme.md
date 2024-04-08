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
Also, you should create a file called `local_settings.py` in the src folder with the configs for the django project