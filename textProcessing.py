from sklearn.feature_extraction.text import CountVectorizer
import numpy
import lda
def main():
    filename = "femaleItalianOutput.txt"

    f = open(filename, "r").read()
    count_vect = CountVectorizer()
    data = [f]
    arrFemale = count_vect.fit_transform(data)
    #f = open("maleItalianOutput.txt, "r").read()
    #count_vect = CountVectorizer()

    #arrMale = count_vect.fit_transform(f)

    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    model.fit(arrFemale)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works
    n_top_words = 8

    for i, topic_dist in enumerate(topic_word):
        topic_words = numpy.array(list(count_vect.vocabulary_.keys()))[numpy.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
