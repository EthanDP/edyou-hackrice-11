from inspect import cleandoc
import tika
from tika import parser
import random

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from string import punctuation
import string

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def parsePDF():
    digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    words = open('MostCommonWords.txt', 'r')
    common_words = words.read().splitlines()
    raw = parser.from_file("USHistory-WEB.pdf")
    content = raw['content']
    split_content = content.split("\n")
    #cleaned_content = [value for value in split_content if value != '' and value != ' ' and value not in punctuation and value[0][0] not in digits and value != '\t']
    cleaned_content = []
    new_split_content = []
    for line in split_content:
        new_line = ''.join(c for c in line if c in string.ascii_letters or c == ' ')
        new_split_content.append(new_line)
    for line in new_split_content:
        unique_word = False
        words = line.split()
        for word in words:
            if word not in common_words:
                unique_word = True
                break

        if line == '' or line == ' ' or line == '\t' or len(line)< 15:
            continue
        elif not unique_word:
            continue
        else:
            cleaned_content.append(line)
    print(cleaned_content)
    search_input = str(random.choices(cleaned_content))
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    print(search_input)
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
        q= search_input
    )
    response = request.execute()
    print("Searched: " + search_input)
    result = "\"" + str(response["items"][0]["snippet"]["title"]) + "\"" + " By: "
    result += str(response["items"][0]["snippet"]["channelTitle"]) + ", "
    result += "https://youtube.com/watch?v=" + str(response["items"][0]["id"]["videoId"])
    print(result)

def handle_pdf_upload(f):
    for chunk in f.chunks():
        print("PDF Received")