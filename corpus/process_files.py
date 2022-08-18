import json
import os
import PyPDF2 
from nltk.tokenize import sent_tokenize, word_tokenize 
from get_files import get_date_from_file

def get_text(pdf_path):   
    # creating a pdf file object 
    pdfFileObj = open(pdf_path, 'rb') 
        
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    total_text = []
    # printing number of pages in pdf file 
    num = pdfReader.numPages 
    for i in range(num):
        # creating a page object 
        pageObj = pdfReader.getPage(i)
        # extracting text from page 
        total_text.append(pageObj.extractText())         
    # closing the pdf file object 
    pdfFileObj.close() 
    return total_text

def get_all_editions(dir = r'corpus\downloads'):
    all = os.listdir(dir)
    editions = {}
    for p in all:
        if p.endswith('.pdf'):
            path = os.path.join(dir, p)
            text = get_text(path)
            date = get_date_from_file(p)
            try:
                editions[date].append(text)
            except KeyError:
                editions[date] = text
    return editions

def get_sentences(text):
    data = get_text(text)
    sen = sent_tokenize(data[0])
    fixed_sentences = []
    for t in sen:
        words = word_tokenize(t)
        fixed_words = []
        for w in words:
            t = w.split('-')
            if len(t) > 1:
                t = t[0]+t[1]
            else:
                t = t[0]
            fixed_words.append(t)
        fixed_sentences.append(fixed_words)

def write_first_json():
    my_dict = get_all_editions()
    with open("data_file.json", "w", encoding = 'utf-8') as write_file:
        json.dump(my_dict, write_file, ensure_ascii=False)

with open("data_file.json", "r", encoding = 'utf-8') as read_it:
    data = json.load(read_it)
    sentence = []
    for d in data.keys:
        all_text = data[d]
        sen = get_sentences(all_text)