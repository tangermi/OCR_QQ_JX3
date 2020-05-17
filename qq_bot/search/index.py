from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import RegexTokenizer, LowercaseFilter , StopFilter, StemFilter
import os
import csv
from jieba.analyse import ChineseAnalyzer

my_analyzer = ChineseAnalyzer()   # chinese analyzer
schema = Schema(question=TEXT(stored=True,analyzer=my_analyzer,field_boost=3.0), answer=TEXT(stored=True,analyzer=my_analyzer))

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = create_in("indexdir",schema)
writer = ix.writer()

with open('qa.csv', encoding='utf-8') as qa:
    reader = csv.reader(qa)
    for row in reader:
        writer.update_document(question=row[0],answer=row[1])

writer.commit()
