from django.db import models
from django.db.models.fields import CharField

class AnnotatedPDF(models.Model):
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(max_length=1000)
