def handle_pdf_upload(f):
    for chunk in f.chunks():
        print("PDF Received")