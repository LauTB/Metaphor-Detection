import json
import os
import PyPDF2 
from nltk.tokenize import sent_tokenize, word_tokenize 
from get_files import get_date_from_file
import spacy
import csv
#nlp = spacy.load("es_core_news_sm")
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
                editions[date] =[ text]
    return editions

def get_sentences(data):
    
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
        fixed_sentences.append(' '. join(f for f in fixed_words))
    return fixed_sentences

def write_first_json():
    my_dict = get_all_editions()
    with open("data_file.json", "w", encoding = 'utf-8') as write_file:
        json.dump(my_dict, write_file, ensure_ascii=False)


def write_sentence_json():
    with open("data_file.json", "r", encoding = 'utf-8') as read_it:
        data = json.load(read_it)
        sentence = []
        for d in data.keys():
            all_text = data[d]
            for text in all_text:
                all_sents = get_sentences(text)
                for sen in all_sents:
                    sentence.append((d, sen))
        with open("sentence_file.json", "w", encoding = 'utf-8') as write_file:
            json.dump(sentence, write_file, ensure_ascii=False)
def create_csv(nlp):
    with open("sentence_file.json", "r", encoding = 'utf-8') as read_it:
        data = json.load(read_it)
        new_data = []
        for date, text in data:
            processed_text = nlp(text)
            tags = []
            for token in processed_text:
                tags.append(token.pos_)
            with open(f'corpus\\csv\\{date}.csv', mode='a', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([date, text, ' '.join(t for t in tags)])

path = r'corpus\csv\2014-05-04.csv'
# with open(path, 'r', encoding = 'utf-8') as csv_file :
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line = 0
#     for row in csv_reader:
#         line+=1
#         if line % 2 == 0:
#             continue
#         p = row[1]
#         text = nlp(p)
#         print(p)
#         noun_adj_pairs = {}
#         for chunk in text.noun_chunks:
#             adj = []
#             noun = ""
#             print(chunk)
#             for tok in chunk:
#                 if tok.pos_ == "NOUN":
#                     noun = tok.text
#                 if tok.pos_ == "ADJ":
#                     adj.append(tok.text)
#             if noun:
#                 noun_adj_pairs.update({noun:adj})
#         print(noun_adj_pairs)
#         input()
get_all_editions()

