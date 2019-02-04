# -*- coding: utf-8 -*-
import MySQLdb, operator
from collections import OrderedDict

db = MySQLdb.connect('localhost', 'root','mysql','cookbook', charset = 'utf8',use_unicode=True)
con = db.cursor()

def lcs(a, b): # Longest common subsequence
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result = a[x-1] + result
            x -= 1
            y -= 1
    return len(result)

def analyzeTagset(textId):
    con.execute("SELECT tags FROM cookbook.tagsets where tagsets.id="+str(textId))
    data = con.fetchone()
    if data: 
        tagset = data[0]
    else:
        tagset = "Przepis nieotagowany!"
        pass
        
    return tagset.replace(",","")

def getIDs(idk):
    ids =[]
    con.execute("select id from cookbook.tagsets where id != "+str(idk)+";")
    data = con.fetchall()
    numrows = con.rowcount
    for i in range(0, numrows):
            ids.append(int(data[i][0]))
    return ids

def compare(firstId):
    results = {}
    originalTags = analyzeTagset(firstId)
    print originalTags
    idsList = getIDs(firstId)

    for pid in idsList:
        results[pid] = (lcs(originalTags, analyzeTagset(pid)))
    results = sorted(results.items(), key = operator.itemgetter(1), reverse = True)
    similarity = []

    for tup in results[0:10]:
        similarity.append(tup[0])

    return similarity

'''db = MySQLdb.connect('localhost', 'root','mysql','cookbook', charset = 'utf8',use_unicode=True)
con = db.cursor()

def buildVector(tags, originalTags):
    originalVector = []
    for tag in tags:
        if tag in originalTags:
            originalVector.append(1)
        else:
            originalVector.append(0)

    return originalVector

def sim(s1,s2):
    commonPos = 0
    for i in range(0,len(s1)):
        if s1[i] == s2[i]:
            commonPos+=1
    return commonPos

def analyzeTagset(textId):
    con.execute("SELECT tags FROM cookbook.tagsets where tagsets.id="+str(textId))
    data = con.fetchone()
    if data: 
        tagset = data[0]
    else:
        tagset = "Przepis nieotagowany!"
        pass
        
    return tagset.split(",")

def compare(firstId):

    originalTags = analyzeTagset(firstId) #tagi z analizowanego przepisu
    #print "Tagi z przepisu: ", originalTags

    con.execute("SELECT tag from cookbook.tags")
    allTags = con.fetchall()
    allTags = [id for sublist in allTags for id in sublist] #wszystkie tagi w BD
    #print "Wszystkie tagi: ", allTags

    vectors = {}
    firstVector = buildVector(allTags, originalTags)

    similarity = {}

    #print "first vec: ", firstVector
    con.execute("SELECT id, tags from cookbook.tagsets where id !="+str(firstId)+";")
    for i in range(0,con.rowcount):
        data = con.fetchone()
        tmpId = data[0]
        tmpTagset = data[1].split(",") #tagi przepisu ktory jest analizowany jako podobny

        #print "\n\nanalizowane ID: ", tmpId
        #print "tmpTagset: ", tmpTagset
        #print "tmpTagset: ", tmpTagset
        vectors[int(tmpId)] = buildVector(allTags, tmpTagset)
        #print "Vector dla przepisu: ",tmpId,":",vectors[int(tmpId)]
        similarity[int(tmpId)]= sim(vectors[int(tmpId)], firstVector)

    sortedSimilarity = OrderedDict(sorted(similarity.items(), key=lambda t: t[1], reverse = True))    
    #print sortedSimilarity
    #print sortedSimilarity.items()
    result = []
    for tup in sortedSimilarity.items():
        result.append(tup[0])

    return result
        
'''