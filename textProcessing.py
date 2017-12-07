# Anne Huang, Natawut Monaikul
# CS 521 Project
# Fall 2017

from sklearn.decomposition import LatentDirichletAllocation
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
    # http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
    # using parameters from http://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py
    matrix = CountVectorizer(stop_words = CUSTOMIZED_STOP_WORDS)
    #matrix = CountVectorizer(max_df=0.95, min_df=2, max_features=1000, stop_words=CUSTOMIZED_STOP_WORDS)
    data = []
    
    if gender == 'MALE':
        data = male(stemmer)
    else:
        data = female(stemmer)

    produceTopics(gender, matrix, matrix.fit_transform(data))

def maleAction(stemmer):
    data = []
    data.append(openFile(stemmer, "AmericanSniper_ChrisKylecleaned.txt"))
    data.append(openFile(stemmer, "Avengers_Malecleaned.txt"))
    data.append(openFile(stemmer, "BourneUltimatum_JasonBournecleaned.txt"))
    data.append(openFile(stemmer, "maleItalianOutputcleaned.txt"))
    print(data)
    return data

def male(stemmer):
    return maleRomance(stemmer)

def female(stemmer):
    return femaleRomance(stemmer)

def maleRomance(stemmer):
    SCRIPTS = ['YouveGotMaleOutputcleaned.txt', 'TitanicMaleOutputcleaned.txt', 'SexCityMaleOutputcleaned.txt', 'PrideMaleOutputcleaned.txt']
    return generateData(stemmer, SCRIPTS)

def femaleRomance(stemmer):
    SCRIPTS = ['YouveGotFemaleOutputcleaned.txt', 'TitanicFemaleOutputcleaned.txt', 'SexCityFemaleOutputcleaned.txt', 'PrideFemaleOutputcleaned.txt']
    return generateData(stemmer, SCRIPTS)

def generateData(stemmer, scripts):
    data = []
    for script in scripts:
        data.append(openFile(stemmer, script))
    return data

def femaleAction(stemmer):
    data = []
    data.append(openFile(stemmer, "AmericanSniper_TayaKylecleaned.txt"))
    data.append(openFile(stemmer, "Avengers_Femalecleaned.txt"))
    data.append(openFile(stemmer, "BourneUltimatum_NickyParsonscleaned.txt"))
    data.append(openFile(stemmer, "femaleItalianOutputcleaned.txt"))
    return data

def openFile(stemmer, filename):
    ret = ""
    f = open(filename, "r").read()
    f = re.sub(r'\d', '', f)
    return f

def produceTopicsSK(gender, count_vect, arr):
    # http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html#sklearn.decomposition.LatentDirichletAllocation
    model = LatentDirichletAllocation(n_topics = 20,  max_iter=5,
                                learning_method='online',
                                learning_offset=50,
                                random_state=0)
    model.fit(arr)
    message = ""

    # Code for printing by
    # Author: Olivier Grisel <olivier.grisel@ensta.org>
    #         Lars Buitinck
    #         Chyi-Kwei Yau <chyikwei.yau@gmail.com>
    #http://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py
    for topic_idx, topic in enumerate(model.components_):
        message += "Topic #%d: " % topic_idx
        message += " ".join([count_vect.get_feature_names()[i]
                             for i in topic.argsort()[:-20 - 1:-1]])
        message += "\n"
    f2 = open(gender + "TopicsSK.txt", "w")
    f2.write(message)
    f2.close()
    
def produceTopics(gender, count_vect, arr):
    # from documentation: http://pythonhosted.org/lda/
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
