from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect

from . import forms
from . import pdf

# Create your views here.
def index(request):
    context = {

    }
    return render(request, "pdf_annotator/index.html", context)

def upload_pdf(request):
    if request.method == "POST":
        form = forms.FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            annotated_file = pdf.handle_pdf_upload(request.FILES['pdf_file'])
            return HttpResponseRedirect("/")

    return HttpResponseBadRequest()

def send_annotated_pdf(request):
    pass