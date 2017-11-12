from sklearn.feature_extraction.text import CountVectorizer
import numpy
import lda

filename = "femaleItalianOutput.txt"

f = open(filename, "r").read()
count_vect = CountVectorizer()

arrFemale = count_vect.fit_transform(f)

#f = open("maleItalianOutput.txt, "r").read()
#count_vect = CountVectorizer()

#arrMale = count_vect.fit_transform(f)

X = numpy.array([arrFemale])

model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
model.fit(X)  # model.fit_transform(X) is also available
topic_word = model.topic_word_  # model.components_ also works
n_top_words = 8

for i, topic_dist in enumerate(topic_word):
    topic_words = numpy.array(count_vect.vocabulary_)[numpy.argsort(topic_dist)][:-n_top_words:-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))
