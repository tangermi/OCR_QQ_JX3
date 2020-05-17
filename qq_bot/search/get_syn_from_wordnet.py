from whoosh.lang.wordnet import Thesaurus
from whoosh.filedb.filestore import FileStorage

def get_syns(text):
    fs = FileStorage("D:\lizi\index_wordnet")
    thesaurus = Thesaurus.from_storage(fs)
    expanded = ''
    for word in text.split():
        try:
            synlist = thesaurus.synonyms(word)
        except:
            synlist = ''
        for syn in synlist:
            expanded = expanded + " " + syn
    return expanded

# test
# expanded = get_syns("fire in the hole")
# print(expanded)