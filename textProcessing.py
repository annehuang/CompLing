from sklearn.feature_extraction.text import CountVectorizer
import numpy
import lda
from nltk.stem.snowball import SnowballStemmer
import re
from preprocessForBTM import CUSTOMIZED_STOP_WORDS

# http://www.nltk.org/howto/stem.html

# this is the list of stop words from SK-Learn
# I am taking out a few: "you" (as in thank you), "very", "first"
#https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/feature_extraction/stop_words.py
# http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/
# "first" comes on in some topics from existing work
# http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf

def glob():
    stemmer = SnowballStemmer("english")
    vectorize('MALE', stemmer)
    vectorize('FEMALE', stemmer)
    
def vectorize(gender, stemmer):
    # English stop words
    count_vect = CountVectorizer(stop_words=CUSTOMIZED_STOP_WORDS)
    data = []
    
    if gender == 'MALE':
        data = male(stemmer)
    else:
        data = female(stemmer)
    
    produceTopics(gender, count_vect, count_vect.fit_transform(data))

def male(stemmer):
    data = []
    data.append(openFile(stemmer, "AmericanSniper_ChrisKylecleaned.txt"))
    data.append(openFile(stemmer, "Avengers_Malecleaned.txt"))
    data.append(openFile(stemmer, "BourneUltimatum_JasonBournecleaned.txt"))
    data.append(openFile(stemmer, "maleItalianOutputcleaned.txt"))
    return data;

def female(stemmer):
    data = []
    data.append(openFile(stemmer, "AmericanSniper_TayaKylecleaned.txt"))
    data.append(openFile(stemmer, "Avengers_Femalecleaned.txt"))
    data.append(openFile(stemmer, "BourneUltimatum_NickyParsonscleaned.txt"))
    data.append(openFile(stemmer, "femaleItalianOutputcleaned.txt"))
    return data;

def openFile(stemmer, filename):
    ret = ""
    f = open(filename, "r").read()
    f = re.sub(r'\d', '', f)
    return f

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
