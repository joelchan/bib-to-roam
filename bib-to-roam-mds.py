from tkinter import Tk
import bibtexparser # dependency, need to pip install
from bibtexparser.bparser import BibTexParser
import pyperclip # dependency, need to pip install
# import getPDF_url as gpdf
import codecs

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
entries = bib.entries
# print(entry)
print(f"Processing {len(entries)} entries")

for entry in entries:
    # parse title
    print(entry)
    title = entry['title'].replace("{", "").replace("}", "").replace("\n", " ")

    # build author string
    authors = []
    for author in entry['author'].split(" and "):
        author = author.strip().replace("\n", " ").split(",")
        authors.append("[[%s %s]]" %(author[-1].strip(), author[0].strip()))

    # get year
    year = "no_info"
    if 'year' in entry:
        year = entry['year'].replace("{", "").replace("}", "")

    # get publication
    entry_type = entry['ENTRYTYPE']
    # key is different for journal articles vs. conference papers; usually I want the series
    et_keys = {
        'article': 'journal',
        'inproceedings': 'booktitle',
        'incollection': 'booktitle'
    }
    et_source_tags = {
        'article': '#ref/Paper',
        'book': '#ref/Book',
        'incollection': '#ref/BookChapter',
        'inproceedings': '#ref/Paper'
    }
    publication = "no_info" # default value for other kinds of pubs
    if entry_type in et_keys:
        publication = entry.get(et_keys[entry_type], "no_info")
        publication = publication.replace("{", "").replace("}", "")
    source_tag = ""
    if entry_type in et_source_tags:
        source_tag = et_source_tags[entry_type]
    else:
        source_tag = "#ref/Other"

    url = ""
    if 'url' in entry:
        url = entry['url']

    # get pdf
    # filename = entry['file'].split(":")[0]
    # embed = gpdf.get_pdf_url(filename)
    embed = "Placeholder"

    abstract = ""
    if "abstract" in entry:
        abstract = entry['abstract']
        abstract = abstract.replace("\n", " ")

    # stitch everything together
    out_str = "- #references\n\t- Title: %s\n\t- Meta:\n\t\t- Tags: %s\n\t\t- Authored by:: %s\n\t\t- Year: [[%s]]\n\t\t- Publication: %s\n\t\t- URL: %s\n\t\t- Citekey: %s\n\t- Content\n\t\t- %s\n\t\t- Abstract\n\t\t\t- %s" %(title, source_tag, " , ".join(authors), year, publication, url, entry['ID'], embed, abstract)

    # write to md
    with codecs.open(f"roam-mds/@{entry['ID']}.md", 'w', encoding='utf8') as outf:
        outf.write(out_str)

# append to the clipboard
r.clipboard_clear()
# pyperclip.copy(out_str)


