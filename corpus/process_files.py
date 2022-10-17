import os
import csv
import spacy
from PyPDF2 import PdfFileReader, PdfFileWriter
from itertools import chain
from get_files import get_date_from_file

nlp = spacy.load("es_core_news_sm")

def join_editions_path(dir = r'corpus\downloads'):
    all = os.listdir(dir)
    editions = {}
    for p in all:
        if p.endswith('.pdf'):
            path = os.path.join(dir, p)
            date = get_date_from_file(p)
            try:
                editions[date].append(path)
            except KeyError:
                editions[date] =[path]
    return editions

def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))
    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

def create_pdfs():
    editions_paths = join_editions_path()
    for date in editions_paths:
        path = os.path.join(r'corpus\pdfs', date+'.pdf')
        merge_pdfs(editions_paths[date],path)

def extract_an_from_pdf(path,save_path):
    with open(path, 'r', encoding = 'utf-8') as csv_file :
        csv_reader = csv.reader(csv_file, delimiter=',')
        an_set = set()
        for row in csv_reader:
            text = row[0]
            doc = nlp(text)
            for token in doc:
                if token.pos_ == 'ADJ':
                    for related in chain(token.lefts, token.rights):
                        if related.pos_ == 'NOUN':
                            pair = (str.lower(token.text), str.lower(related.text))
                            an_set.add(pair)
        with open(save_path, 'w+', encoding = 'utf-8', newline='') as csv_save_file :
            csv_writer = csv.writer(csv_save_file)
            csv_writer.writerows(list(an_set))
