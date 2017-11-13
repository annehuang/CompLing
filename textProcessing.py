from sklearn.feature_extraction.text import CountVectorizer
import numpy
import lda

def main():
    produceTopics("femaleItalian")
    produceTopics("maleItalian")

def produceTopics(filen):
    filename = filen + "Output.txt"

    f = open(filename, "r").read()
    count_vect = CountVectorizer()
    data = [f]
    arr = count_vect.fit_transform(data)

    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    model.fit(arr)
    topic_word = model.topic_word_
    n_top_words = 8

    out = ""
    for i, topic_dist in enumerate(topic_word):
        topic_words = numpy.array(list(count_vect.vocabulary_.keys()))[numpy.argsort(topic_dist)][:-n_top_words:-1]
        out += 'Topic {}: {}'.format(i, ' '.join(topic_words))
        out += '\n'

    f2 = open(filen + "Topics.txt", "w")
    f2.write(out)
    f2.close()
