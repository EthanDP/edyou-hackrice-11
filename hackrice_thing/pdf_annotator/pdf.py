import random
import string
import os
from io import StringIO

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from tika import parser
from pathlib import Path
from io import StringIO
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileWriter, PdfFileReader
from .PyPDF2Highlight import createHighlight, addHighlightToPage


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def parse_pdf(pdf_path, result_path):
    words = open("pdf_annotator/MostCommonWords.txt", 'r')
    common_words = words.read().splitlines()
    file_data = []
    _buffer = StringIO()
    data = parser.from_file(pdf_path, xmlContent=True)
    xhtml_data = BeautifulSoup(data['content'])
    for page, content in enumerate(xhtml_data.find_all('div', attrs={'class': 'page'})):
        print("Parsing: " + str(page+1))
        _buffer = StringIO()
        _buffer.write(str(content))
        parsed_content = parser.from_buffer(_buffer.getvalue())
        if parsed_content['content'] != None:
            text = parsed_content['content'].strip()
        file_data.append({'id': str(page+1), 'content': text})

    new_pages = []
    for page in file_data:
        new_lines = []
        for line in page['content'].split("\n"):
            new_line = ''.join(c for c in line if c in string.ascii_letters or c == ' ')
            new_lines.append(new_line)
        new_pages.append((new_lines, page['id']))
        print("Cleaning Characters: " + str(page['id']))

    cleaned_pages = []
    for page in new_pages:
        cleaned_page = []
        for line in page[0]:
            unique_word = False
            words = line.split()
            for word in words:
                if word not in common_words:
                    unique_word = True
                    break

            if line == '' or line == ' ' or line == '\t' or len(line) < 15:
                continue
            elif not unique_word:
                continue
            else:
                cleaned_page.append(line)
        cleaned_pages.append((cleaned_page, page[1]))
        print("Cleaning Lines: " + str(page[1]))

    pdfInput = PdfFileReader(open(pdf_path, "rb"))
    pdfOutput = PdfFileWriter()

    for page in cleaned_pages:
        new_page = pdfInput.getPage(int(page[1])-1)
        if page[0] == []:
            annotation = "No relevant topics"
        else:
            annotation = youtube_search(page[0][0])
        highlight = createHighlight(0, 792, 100, 692, {
            "author": "",
            "contents": annotation
        })

        addHighlightToPage(highlight, new_page, pdfOutput)

        pdfOutput.addPage(new_page)
        print("Writing Annotations: " + str(page[1]))
        if page[1] == '10':
            break

    outputStream = open(result_path, "wb+")
    pdfOutput.write(outputStream)

def youtube_search(search):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_533721667580-gd42cojl1vvhk64a4t0q7pr9bjddaj5p.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q = search
    )
    response = request.execute()
    if "videoId" not in response["items"][0]["id"].keys():
        return "No relevant topics"
    result = "\"" + str(response["items"][0]["snippet"]["title"]) + "\"" + " By: "
    result += str(response["items"][0]["snippet"]["channelTitle"]) + ", " 
    result += "https://youtube.com/watch?v=" + str(response["items"][0]["id"]["videoId"])
    return result

def handle_pdf_upload(f):
    result_filename = str(Path(str(f)).with_suffix("")) + "_annotated.pdf"
    temp_dir = os.getcwd() + "\\pdf_annotator\\temp\\"
    temp_path = temp_dir + "temp.pdf"
    result_path = temp_dir + result_filename
    with open(temp_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    parse_pdf(temp_path, result_path)
    os.remove(temp_path)
    return (result_path, result_filename)

    