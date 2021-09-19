# edYou
A website and PDF parser tool that allows you to upload a pdf of a textbook or similar academic text and receive an annotated copy with links to relevant YouTube videos throughout the document. Created for HackRice 11

# Contributors
Ethan Peck (edp2@rice.edu): Web development, file uploading and downloading, integration with PDF parser  
Bryant Cassady (jbc8@rice.edu): PDF Parsing, PDF annotation, integration with YouTube API

# Submission Description
## Inspiration
Every college student has had an experience with a particularly boring section of a textbook. The ones where you find yourself reading the same sentence over and over again yet still not understanding the material. We were inspired by this feeling to create a tool that makes it easy to find useful videos relating to the content you are reading about.

## What it does
edYou is a website and PDF tool that can annotate nearly any type of academic textbook or document with links to relevant YouTube videos on every page. All it takes to use is uploading a pdf of the file you want annotated and a short wait while our program parses and pulls key words from each page. You will then have the option to download a fully annotated copy filled with useful YouTube links.

## How we built it
edYou is based on Python and the Django web framework. We also used html and css for page styling and the upload form. Among some of the libraries and technologies we used are Tika, PyPDF2, and Beautiful Soup 4 for parsing, the Google oauth and Youtube APIs for finding relevant videos, and a Google Cloud Compute Engine virtual machine for hosting our website (we are running Ubuntu 20.04).

## Challenges we ran into
PDF parsing was by far the toughest challenge in developing edYou. The PDF file format is not intended to be as easy to edit as say a text or doc file. We ran into many issues with text being unreadable and a general lack of official support for PDF parsing in Python. We had to settle for a third party fork of Tika that had some improved functionality. In the end we were able to read most of the information from every PDF we uploaded.

Another issue that we are still trying to solve is the quota limit with the YouTube API. With our basic account we have a quota limit of 10,000. Every search takes up 100 quota points which means that until we are approved for a higher quote we can only complete roughly 100 searches per day. This is severely limiting and something we hope to fix soon.

## Accomplishments that we're proud of
Completing a fully fledged project in less than two days was a really fulfilling experience. We ran into a lot of problems throughout the 36 hour period and we are proud of the ways in which we solved or worked around them.

## What we learned
We learned a ton about what it takes to complete a full project in a weekend as well as how to find unique solutions to setbacks encountered during development.

## What's next for edYou
The next features we need to implement are improving the annotation system to insert hyperlinks directly into the document and finding a way to increase our YouTube API quota limit.
