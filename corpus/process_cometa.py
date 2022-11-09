import csv
import spacy
from itertools import chain
nlp = spacy.load("es_core_news_sm")

def map_annotations(ann):
    if ann == 'O':
        return 0
    return 1

def pair_sentence(sen):
    sentence = []
    tags = []
    for s,t in sen:
        sentence.append(s)
        tags.append(t)
    return (sentence,tags)

def create_tagged_sentence():
    file = open(r'corpus\CoMeta\cometa_test.tsv', encoding='UTF-8')
    cs = csv.reader(file, delimiter="\t")
    sentences = []
    sentence = []
    for row in file:
        line = row.split()
        if line == []:
            continue
        if line[0] == '.':
            sentences.append(sentence)
            sentence = []
            continue
        sentence.append((line[0], map_annotations(line[1])))

    sents = []
    tag = []
    for sen in sentences:
        s,t = pair_sentence(sen)
        sents.append(s)
        tag.append(t)

    with open('corpus\CoMeta\tagged_sents.txt', 'w+', encoding='utf-8') as file:
        for i in range(len(sents)):
            file.write(' '.join(sents[i])+' $ '+ ' '.join(str(t) for t in tag[i])+ '\n')

def create_formatted_data(path):
    an_set = set()
    data = []
    with open(path, 'r') as f:
        data = f.readlines()
    for d in data:
        sen, tag = d.split('$')
        tag = tag.split()
        doc = nlp(sen)
        for token in doc:
            if token.pos_ == 'ADJ':
                for related in chain(token.lefts, token.rights):
                    if related.pos_ == 'NOUN':
                        pair = (str.lower(token.text), str.lower(related.text), str(max(int(tag[token.i]),int(tag[related.i]))))
                        an_set.add(pair)
    return an_set

def format_data(path, save_path):
    data = create_formatted_data(path)
    with open(save_path, 'w') as f:
        for d in data:
            f.write(' '.join(d)+'\n')