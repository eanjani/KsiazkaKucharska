# -*- coding: utf-8 -*-
from pandas import DataFrame
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from .models import Przepisy
import MySQLdb

db = MySQLdb.connect('localhost', 'root','mysql','cookbook', charset = 'utf8',use_unicode=True)
con = db.cursor()
    
def readFromDB(idk):
    con.execute("SELECT * FROM cookbook.app_przepisy where app_przepisy.id="+str(idk))
    data = con.fetchone()
    rawText = data[2]
    yield rawText
    
def buildDataFrame(idk,classification):
    rows = []
    index = []
    for rawText in readFromDB(idk):
        rows.append({'text':rawText, 'class':classification})
        index.append(idk)
    
    dataFrame = DataFrame(rows, index = index)
    return dataFrame

def classifyText(textId):
    CIASTO = "ciasto"
    DESER = "deser"

    SOURCES = [ # oparciu o przepisy
        (18, CIASTO),
        (19, CIASTO),
        (20, CIASTO),
        (25, DESER),
        (32, CIASTO),
        (31, CIASTO),
        (38, DESER),
        (46, DESER),
        (50, DESER),
        (52, DESER),
        ]

    data = DataFrame({'text':[],'class':[]})
    for idk, classification in SOURCES:
        data = data.append(buildDataFrame(idk, classification))

    data = data.reindex(numpy.random.permutation(data.index))

    count_vectorizer = CountVectorizer()
    counts = count_vectorizer.fit_transform(data['text'].values)

    classifier = MultinomialNB()
    targets = data['class'].values
    classifier.fit(counts, targets)

    con.execute("SELECT * FROM cookbook.app_przepisy where app_przepisy.id="+str(textId))
    data = con.fetchone()
    rawText = data[2]
        
    examples=[rawText]
    example_counts = count_vectorizer.transform(examples)
    predictions = classifier.predict(example_counts)
    #print data[1], "zaklasyfikowano jako: ", predictions
    #con.close()

    katid = ""
    if predictions[0] == CIASTO:
        katid = 1
    else:
        katid = 2


    #obj = Przepisy.objects.get(id = textId)
    #obj.kategoria_id = katid
    #obj.save()
    #con.execute("UPDATE cookbook.app_przepisy SET kategoria_id ="+str(katid)+" WHERE id="+str(textId)) #czemu nie dziala?
    return predictions[0]
