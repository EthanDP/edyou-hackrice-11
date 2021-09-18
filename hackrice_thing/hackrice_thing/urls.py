from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('', include('pdf_annotator.urls')),
    path('api/upload_pdf', include('pdf_annotator.urls')),
    path('admin/', admin.site.urls),
]
