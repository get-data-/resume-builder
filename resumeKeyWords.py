# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 12:52:05 2015
note: this is my first time writing code. I'd appreciate any tips on how I might be able to do this better
@author: 케빈
"""

from bs4 import BeautifulSoup
import requests
#import html5lib
import csv
import nltk
from nltk import FreqDist
import re
import time
oneMoreAgain = open('C:/filePathGoesHere/visitedLinks.txt', 'r')
beenThere = [oneMoreAgain.read()]
oneMoreAgain.close()
onTheWay = []
contentArray = []
##sampleCollector asks the user what job they want and collects samples from www.indeed.com
def sampleCollector():
    dream = raw_input("what is your dream job?").replace(" ","+")
    site = "http://www.indeed.com"
    theSite =site+"/jobs?q="+dream
    html = requests.get(theSite).text
    soup = BeautifulSoup(html)
    #print(soup.get_text())
    for link in soup.find_all('a', href=True):
        if link in beenThere:
            pass 
        else:
            url = link['href']
            qualifiedLink = site+url
            match1 = re.findall(r'http://www.indeed.com/rc/*.*', qualifiedLink)
            if match1:
                #print match1
                onTheWay.append(match1)
                #print "match1","\n", match1, "\n"
            match2 = re.findall(r'http://www.indeed.com/cmp/*.*', qualifiedLink)
    
            if match2:
                #print "match2", "\n", match2, "\n"
                onTheWay.append(match2)
            #print "adding ", url, " to the list", "\n"
##processor takes links to job posts acquired from sampleCollector, parses the results, and writes the results to a txt file
def processor():
    for sample in onTheWay:
        item = ''.join(str(e) for e in sample)
        print "Working on ", item, "\n"
        if item in beenThere:
            pass
        else:
            try:                  
                data = requests.get(item).text
                raw = BeautifulSoup(data, 'html5lib')
                content = re.findall(r'<p.*?>(.*?)</p>', str(raw))
                for lines in content:
                    #print str(lines).strip('<b>').strip('</b>')
                    contentArray.append(str(lines).strip('<b>').strip('</b>'))
                content2 = re.findall(r'<li>(.*?)</li>', str(raw))
                for line in content2:
                    #print line
                    contentArray.append(line)
                beenThere.append(item)
                with open('C:/filePathGoesHere/visitedLinks.txt','wb') as f:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerow([beenThere,])
                    f.close()
                with open('C:/filePathGoesHere/a.txt','wb') as k:
                    writer = csv.writer(k, delimiter=',')
                    writer.writerow([contentArray,])
                    k.close() 
            except Exception, e:
                print str(e)
#dontForgetTheSave is going to save the Natural Language Processed Results
#def dontForgetTheSave():
#print str(exampleArray).encode('ascii', 'ignore')
#processLanguage uses NLP to sort out 1,2,3 key word and geopolitical term frequency
def processLanguage():
    fob = open('C:/filePathGoesHere/a.txt', 'r')
    exampleArray = [fob.read()]
    fob.close()
    try:
        for item in exampleArray:
            tokenized = nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            namedEnt = nltk.ne_chunk(tagged, binary = True)
            chunkGram = r"""
    Chunk:
        {<NN\w?>*<JJ>*<NN>}
        {<NNP>+}
        {<NN?>+}
        {<NE>+}
        {<DT|PP\$>?<JJ>*<NN>}
        """
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)           
            oneWordTerm = re.findall(r'\(Chunk\s(\w*?)/',str(chunked))
            oneWordFreq = FreqDist(oneWordTerm)
            twoWordTerm = re.findall(r'\(Chunk\s(.*?)/\w+\s(.*?)/\w+\)',str(chunked))
            twoWordFreq = FreqDist(twoWordTerm)
            threeWordTerm = re.findall(r'\(Chunk\s(.*?)/\w+\s(.*?)/\w+\s(.*?)/\w+\)',str(chunked))
            threeWordFreq = FreqDist(threeWordTerm)
            oneEntities = re.findall(r'\(NE\s(.*?)/\w*?\)',str(namedEnt))
            oneEntFreq = FreqDist(oneEntities)
            twoEntities = re.findall(r'\(NE\s(.*?)/\w+\s(.*?)/\w+\)',str(namedEnt))
            twoEntFreq = FreqDist(twoEntities)
            threeEntities = re.findall(r'\(NE\s(.*?)/\w+\s(.*?)/\w+\s(.*?)\w+\)',str(namedEnt))
            threeEntFreq = FreqDist(threeEntities)
##Now to poop out the results            
            print "\n+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*"
            print "Key Word Search"
            print "+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*\n"
            print "**********************************"
            print "One word search terms"
            print "**********************************"
            print oneWordFreq
            print oneWordTerm
            print "**********************************"
            print "Two word search terms"
            print "**********************************"
            print twoWordFreq
            print twoWordTerm
            print "***********************************"
            print "Three word search terms"
            print "**********************************"
            print threeWordFreq
            print threeWordTerm          
            print "\n+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*"
            print "Named Entity / Geopolitical Search Terms"
            print "+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*\n"
            print "*******************************"
            print "One Word Terms"
            print "*******************************"
            print oneEntFreq            
            print oneEntities
            print "*******************************"
            print "Two Word Terms"
            print "*******************************"
            print twoEntFreq            
            print twoEntities
            print "*******************************"
            print "Three Word Terms"
            print "*******************************"
            print threeEntFreq            
            print threeEntities
            print "*******************************"
    except Exception, e:
            print str(e)
       
#main runs this collection of scripts
def main():
    sampleCollector()
    processor()
    time.sleep(10)
    processLanguage()

main()

print "did it work?", "\n"
