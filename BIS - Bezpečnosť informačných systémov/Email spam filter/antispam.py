#!/usr/bin/env python3
import email
import sys
import pickle

from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

def getKeywords(emailContent):
    keywords = dict()
    tokens=getTokens(emailContent)
    lemmatized=lemmatize(tokens)
    stopWordsList = stopwords.words("english")

    for token in lemmatized:
        if(token not in stopWordsList):
            keywords[token]=True
    return keywords

def getTokens(emailContent):
    tokens = word_tokenize(emailContent)
    return tokens

def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatizedTokens=[]
    for token in tokens:
        lemmatizedTokens.append(lemmatizer.lemmatize(token.lower()))
    return lemmatizedTokens

def getEmail(emailMessage):
    try:
        f = open(emailMessage, 'r')
    except:
        return False,"could not open file"
    try:
        msg = email.message_from_file(f)
    except:
        return False, "could not parse email - email.message_from_string() exception"


    try:
        wholeMsg = ''
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                wholeMsg += (part.get_payload())
        wholeMsg += (msg['subject'])
        return wholeMsg,""
    except:
        return False, "error parsing email"


f = open('classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()



for i in range(1,len(sys.argv)):
    emailContent,error=getEmail(sys.argv[i])
    if(emailContent!=False):
        keywords = getKeywords(emailContent)
        print(sys.argv[i],end="")
        print(" - ",end="")
        print(classifier.classify(keywords))
    else:
        print(sys.argv[i],end="")
        print(" - FAIL - ",end="")
        print(error)
