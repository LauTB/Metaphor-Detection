import random

ACCEPTED_LABEL = '1'
REJECTED_LABEL = '0'

class ANCORPUS():
    '''
    Corpus created with data from 
    https://github.com/ytsvetko/metaphor
    '''
    def __init__(self) -> None:
        self.data = []
        self.data_lables = []

    def load_data(self, filepath):
        with open(filepath, 'r') as file:
            raw_data = file.read().splitlines()
            for d in raw_data:
                data = d.split()
                self.data.append((data[0],data[1]))
                self.data_lables.append(data[-1])
    
    def transform_data(self, embeddings):
        transformed = []
        for d in self.data:
            t= embeddings.embeddings(d)
            transformed.append(t)
        return transformed

def load_anmet_nomet(nomet_filepath, met_filepath):
    mets = []
    nomets = []
    with open(met_filepath, 'r') as file:
        mets = file.read().splitlines()
    with open(nomet_filepath, 'r') as file:
        nomets = file.read().splitlines()
    return mets, nomets
def join_mets_nomets(mets, nomets):
    joined = []
    r = random.Random()
    while mets and nomets :
        met = r.choice(mets)
        mets.remove(met)
        nomet = r.choice(nomets)
        nomets.remove(nomet)
        order = r.random()
        if order <= 0.5:
            joined.append(met)
            joined.append(nomet)
        else:
            joined.append(nomet)
            joined.append(met)
    remain = []
    if mets:
        remain = mets
    elif nomets:
        remain = nomets
    while remain:
        rem = r.choice(remain)
        remain.remove(rem)
        joined.append(rem)
    return joined
def create_joined_file(joined, filename, filepath='model\data'):
    path = filepath + '\\' + filename +'.txt'
    with open(path,'w') as f:
        for join in joined:
            f.write("%s\n" % str(join))    
def label(elements, label):
    labeled = []
    for elem in elements:
        labeled.append(elem + ' ' + label)
    return labeled
def prepare_an_met():
    an_met, an_nomet =  load_anmet_nomet(r'model\data\an_nonmets.txt',r'model\data\an_mets.txt')
    met = label(an_met,ACCEPTED_LABEL)
    nomet = label(an_nomet, REJECTED_LABEL)
    joined = join_mets_nomets(met, nomet)
    create_joined_file(joined, 'an_joined')

t = ANCORPUS()
t.load_data(r'model\data\an_joined.txt')
