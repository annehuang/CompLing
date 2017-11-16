from sklearn.feature_extraction.text import CountVectorizer
import numpy
import lda
from nltk.stem.snowball import SnowballStemmer
import re

# http://www.nltk.org/howto/stem.html

def glob():
    stemmer = SnowballStemmer("english")
    vectorize('MALE', stemmer)
    vectorize('FEMALE', stemmer)
    
def vectorize(gender, stemmer):
    # English stop words
    count_vect = CountVectorizer(stop_words="english")
    data = []
    
    if gender == 'MALE':
        data = male(stemmer)
    else:
        data = female(stemmer)
    
    produceTopics(gender, count_vect, count_vect.fit_transform(data))

def male(stemmer):
    data = []
    data.append(openFile(stemmer, "AmericanSniper_ChrisKyle.txt"))
    data.append(openFile(stemmer, "Avengers_Male.txt"))
    data.append(openFile(stemmer, "BourneUltimatum_JasonBourne.txt"))
    data.append(openFile(stemmer, "maleItalianOutput.txt"))
    return data;

def female(stemmer):
    data = []
    data.append(openFile(stemmer, "AmericanSniper_TayaKyle.txt"))
    data.append(openFile(stemmer, "Avengers_Female.txt"))
    data.append(openFile(stemmer, "BourneUltimatum_NickyParsons.txt"))
    data.append(openFile(stemmer, "femaleItalianOutput.txt"))
    return data;

def openFile(stemmer, filename):
    ret = ""
    f = open(filename, "r").read()
    f = re.sub(r'\d', '', f)
    for word in f:
        ret += stemmer.stem(word)
    return ret

def produceTopics(gender, count_vect, arr):
    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    model.fit(arr)
    topic_word = model.topic_word_
    n_top_words = 8

    out = ""
    for i, topic_dist in enumerate(topic_word):
        topic_words = numpy.array(list(count_vect.vocabulary_.keys()))[numpy.argsort(topic_dist)][:-n_top_words:-1]
        out += 'Topic {}: {}'.format(i, ' '.join(topic_words))
        out += '\n'

    f2 = open(gender + "Topics.txt", "w")
    f2.write(out)
    f2.close()
