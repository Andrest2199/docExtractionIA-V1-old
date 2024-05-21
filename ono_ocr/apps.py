from django.apps import AppConfig
from ono_ocr.thresholds import length_threshold_calculator
from django.conf import settings
import os


class OnoOcrConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ono_ocr"

    def ready(self):
        filepath= os.path.dirname(os.path.abspath(__file__))
        data_inject_folder = os.path.join(filepath, "data_inject")
        length_threshold_calculator(data_inject_folder)
