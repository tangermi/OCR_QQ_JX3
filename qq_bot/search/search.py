from whoosh.fields import *
from whoosh import qparser
from whoosh.qparser import QueryParser,MultifieldParser
from whoosh.index import create_in
from whoosh.lang.wordnet import Thesaurus
from search.get_syn_from_wordnet import get_syns

import whoosh.index as index
ix = index.open_dir("indexdir")

def search(query_text, expansion=False):
    with ix.searcher() as searcher:
        og = qparser.OrGroup.factory(0.8)
        parser = MultifieldParser(["question","answer"], ix.schema,group=og)
        # parser.add_plugin(qparser.FuzzyTermPlugin())
        if expansion:
            query_expanded = ''
            # get synonyms for the query text
            syns = get_syns(query_text)

            for word in query_text.split():
                boosted_word = word + '^3'
                query_expanded = query_expanded + ' ' + boosted_word
            query_expanded = query_expanded + syns
            print(f'Search for: {query_expanded}')
            query = parser.parse(query_expanded)
        else:
            query = parser.parse(query_text)
            print(f'Search for: {query_text}')

        results = searcher.search(query, limit=1)

        # runtime = results.runtime
        # transform the data structure to a list of dictionary so it can be accessed while reader closed
        answer = ''
        for passage in results:
           answer += ''.join([passage['question'], '\n', passage['answer']])
        return answer