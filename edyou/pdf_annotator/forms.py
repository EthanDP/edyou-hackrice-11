from django import forms

class FileUploadForm(forms.Form):
    pdf_file = forms.FileField()