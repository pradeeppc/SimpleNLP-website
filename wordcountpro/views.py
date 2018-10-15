from django.http import HttpResponse
from django.shortcuts import render
import operator
import nltk

import re
from nltk.probability import FreqDist
from nltk.util import ngrams
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

def home(request):
    return render(request,'home.html')
def count(request):
    fulltext = request.GET['fulltext']
    tknzr = TweetTokenizer() 
    review_tokens = tknzr.tokenize(fulltext)
    print(len(fulltext))
    punctuation = re.compile(r'[-.?!,":;()|0-9]')

    review_tokens2 = []
    for token in review_tokens:
        word = punctuation.sub("", token)
        if len(word)>0:
            review_tokens2.append(word)
            
            print(len(review_tokens2))

    review_tokens3 = [ ]
    stp_words = set(stopwords.words('english'))

    for token in review_tokens2:
        token = token.lower()
        if token not in stp_words:
            review_tokens3.append(token)
    print(review_tokens3)
    
    fdist = FreqDist()
    for word in review_tokens3:
        fdist[word] += 1
    len(fdist)
    fdist_top20 = fdist.most_common(20)
    print(fdist_top20)

    pos_list = []
    for token in review_tokens3:
        pos_list.append(nltk.pos_tag([token]))
    len(pos_list)
    print(pos_list[1:20])
    #len(pos_list)
    #print(pos_list[10])

    pos_set = set()
    for pos in pos_list:
        pos_set.add(pos[0][1])
    len(pos_set)
    print(pos_set)

 
    pos_JJ = []
    for each_POS in pos_list:
        if each_POS[0][1] in ["JJ", "JJR","JJS"]:
            pos_JJ.append(each_POS[0][0])
    pos_JJ

    noun = []
    for each_POS in pos_list:
        if each_POS[0][1] in ["JJ", "JJR","JJS"]:
            pos_JJ.append(each_POS[0][0])
    pos_JJ

    fdist_JJ = FreqDist()
    for word in pos_JJ:
        fdist_JJ[word] += 1
    len(fdist_JJ)
    fdist_JJ_top20 = fdist_JJ.most_common(20)
    fdist_JJ_top20

    word_lem = WordNetLemmatizer()
    lem_ADJ = []
    lem_ADV = []
    lem_VERB = []
    for word in review_tokens3:
        word_pos = nltk.pos_tag([word])
        
        if word_pos[0][1] in ["JJ", "JJR", "JJS"]:
            lem_ADJ.append((word_pos[0][0], word_lem.lemmatize(word, wordnet.ADJ)))
            
        if word_pos[0][1] in ["RB", "RBR", "RBS"]:
            lem_ADV.append((word_pos[0][0], word_lem.lemmatize(word, wordnet.ADV)))

        if word_pos[0][1] in ["VB", "VBD", "VBN","VBZ"]:
            lem_VERB.append((word_pos[0][0], word_lem.lemmatize(word, wordnet.VERB)))
    len(lem_ADJ)
    print(lem_ADJ[1:10])
    len(lem_ADV)
    print(lem_ADV[1:10])
    len(lem_VERB)
    print(lem_VERB[1:10])





    wordlist = fulltext.split()
    worddict ={}
    for word in wordlist:
        if word in worddict:
            worddict[word] += 1
        else:
            worddict[word] = 1
    
    # lem = ({'lem_ADJ[:10]':lem_ADJ[:10],'lem_ADV[:10]':lem_ADV[:10],'lem_VERB[:10]':lem_VERB[:10]})
    #sortedwords=sorted(worddict.items(), key=operator.itemgetter(1),reverse=True)
    #return render(request,'count.html',{'fulltext':fulltext,'count':len(wordlist),'sortedwords':sortedwords})
    return render(request,'count.html',{'fulltext':fulltext,'count':len(wordlist),'fdist_top20':fdist_top20,'pos_list':pos_list[1:20],'pos_set':pos_set,'pos_JJ':pos_JJ,'fdist_JJ_top20':fdist_JJ_top20,'lem_ADJ':lem_ADJ[1:10],'lem_ADV':lem_ADV[1:10],'lem_VERB':lem_VERB[1:10]})