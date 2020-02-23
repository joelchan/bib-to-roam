from tkinter import Tk
import bibtexparser # dependency, need to pip install
from bibtexparser.bparser import BibTexParser
import pyperclip # dependency, need to pip install

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

# parse title
title = entry['title'].replace("{", "").replace("}", "")

# build author string
authors = []
for author in entry['author'].split(" and "):
    author = author.strip().split(",")
    authors.append("%s %s" %(author[-1], author[0]))

# get year
year = entry['year'].replace("{", "").replace("}", "")

# get publication
entry_type = entry['ENTRYTYPE']
# key is different for journal articles vs. conference papers; usually I want the series
et_keys = {
    'article': 'journal',
    'inproceedings': 'series',
    'incollection': 'series'
}
publication = "no_info" # default value for other kinds of pubs
if entry_type in et_keys:
    publication = entry[et_keys[entry_type]].replace("{", "").replace("}", "")

# stitch everything together
out_str = "- Metadata\n\t - Title: %s\n\t - Authored by:: %s\n\t - Year: %s\n\t - Publication: %s" %(title, " , ".join(authors), year, publication)

# append to the clipboard
r.clipboard_clear()
pyperclip.copy(out_str)
