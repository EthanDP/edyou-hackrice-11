import os

from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseServerError

from . import forms
from . import pdf

# Create your views here.
def index(request):
    context = {}
    return render(request, "pdf_annotator/index.html", context)

def upload_pdf(request):
    if request.method == "POST":
        form = forms.FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            annotated_file_data = pdf.handle_pdf_upload(request.FILES['pdf_file'])
            with open(annotated_file_data[0], "rb") as result:
                response = HttpResponse(result, content_type="application/json")
                response['Content-Disposition'] = "attachment; filename=" + annotated_file_data[1]
                os.remove(annotated_file_data[0])
                return response

    return HttpResponseBadRequest()

def send_annotated_pdf(request):
    pass