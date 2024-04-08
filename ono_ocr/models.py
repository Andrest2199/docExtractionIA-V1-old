from django.db import models
import json


class Extraction(models.Model):
    doctype = models.CharField(max_length=10)
    original_filename = models.CharField(max_length=100)
    ocr = models.CharField(max_length=20)
    entity_recognition = models.CharField(max_length=25)
    # accuracy = models.FloatField()
    values = models.JSONField()
    raw_text = models.TextField()

    def to_json(self):
        return {
            "doctype": self.doctype,
            "original_filename": self.original_filename,
            # "ocr": self.ocr,
            "entity_recognition": self.entity_recognition,
            "values": self.values,
            "raw_text": self.raw_text,
        }

    def __str__(self):
        return self.doctype
