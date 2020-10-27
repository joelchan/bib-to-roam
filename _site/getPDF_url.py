from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from tkinter import Tk
import bibtexparser # dependency, need to pip install
from bibtexparser.bparser import BibTexParser
import pyperclip # dependency, need to pip install
import getPDF_url as gpdf

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def get_pdf_url(filename):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gdrive api credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    # results = service.files().list(
    #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # items = results.get('files', [])

    results = service.files().list(q="name='" + filename + "'",
        spaces='drive',
        fields='nextPageToken, files(id, name)').execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
        return None
    else:
        print('Files:')
        # pdf_embed = """:hiccup [:iframe {:width "650px", :height "650px", :src "https://drive.google.com/file/d/%s/preview"}]""" %items[0]['id']
        pdf_embed = "{{iframe: https://drive.google.com/file/d/%s/preview}}" %items[0]['id']
        #for item in items:
        #    print(u'{0} ({1})'.format(item['name'], item['id']))
        return pdf_embed

if __name__ == '__main__':
    # get citation from clipboard
    # we assume it is in valid bibtex
    # we assume has title, authors, year, and publication; lazy for now, should add edge cases later
    r = Tk()
    r.withdraw()
    clip_text = r.clipboard_get()

    # parse the bibtex
    # need to define a parser with custom settings bc zotero has nonstandard bibtex items like "jan" for month
    # per https://github.com/sciunto-org/python-bibtexparser/issues/192
    parser = BibTexParser(common_strings=True)
    bib = bibtexparser.loads(clip_text, parser)
    entry = bib.entries[0]

    filename = entry['file'].split(":")[0]
    embed = gpdf.get_pdf_url(filename)

    r.clipboard_clear()
    pyperclip.copy(embed)