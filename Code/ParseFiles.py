from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import lda
import re, os
import random
from nltk.tokenize import word_tokenize, WordPunctTokenizer, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.parse.stanford import StanfordDependencyParser

# Extract information from the movie_lines.txt file
def movie_lines(file):
	f = open(file)
	lines = f.readlines()
	f.close()
	d = {}
	for line in lines:
		l = line.strip().split(" +++$+++ ")
		if len(l) == 4:
			lid, cid, mid, name = l
			text = ""
		elif len(l) == 5:
			lid, cid, mid, name, text = l
		d[lid] = {"cid": cid, "mid": mid, "name": name, "text": text}
	return d
	

# Extract information from the movie_titles_metadata.txt file
def movie_titles_metadata(file):
	f = open(file)
	lines = f.readlines()
	f.close()
	d = {}
	for line in lines:
		mid, title, year, rating, votes, genres = line.strip().split(" +++$+++ ")
		genres = genres.strip("[]'").split("', '")
		genres = map(lambda l: l.lower(), genres)
		d[mid] = {"title": title, "year": year, "rating": rating, "votes": votes, "genres": genres}
	return d
	
	
# Extract information from the movie_characters_metadata.txt file
def movie_characters_metadata(file):
	f = open(file)
	lines = f.readlines()
	f.close()
	d = {}
	for line in lines:
		cid, name, mid, title, gender, position = line.strip().split(" +++$+++ ")
		gender = gender.lower()
		d[cid] = {"name": name, "mid": mid, "title": title, "gender": gender, "position": position}
	return d
	
	
# Match up information from all files to get lines from only one gender in a specific genre
def gender_lines(lines, titles, chars, file, gender, genre):
	l = []
	for lid, info in lines.iteritems():
		if chars[info["cid"]]["gender"] == gender and genre in titles[info["mid"]]["genres"]:
			l.append(info["text"])
	f = open(file, "w")
	for line in l:
		f.write(line + "\n")
	f.close()
	
	
# Remove non-alphanumeric characters, html tags like <i></i>, and anything else
def clean_file(in_file, out_file):
	f = open(in_file)
	lines = map(lambda x: x.strip(), f.readlines())
	f.close()
	f = open(out_file, "w")
	for line in lines:
		new_line = re.sub("<.+?>|\[.+?\]", "", line)
		new_line = re.sub("[^A-Za-z0-9'\s\.\?!\"\-,\:;]", " ", new_line)
		#new_line = new_line.strip()
		#new_line = re.sub("^' | '$", "", new_line)
		#new_line = re.sub(" ' ", " ", new_line)
		new_line = re.sub("\s\s+", " ", new_line)
		f.write(new_line.strip() + "\n")
	f.close()
	
# Source: this is adapted from the list of stop words from SK-Learn
# https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/feature_extraction/stop_words.py	
CUSTOMIZED_STOP_WORDS = [
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "aren't",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "co", "con","couldnt",
    "cry", "de", "describe", "detail", "did", "didn't", "do", "don't", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go", "going", "got",
    "had", "has", "hasnt", "have", "he", "he'll", "he's", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "id", "ie", "if", "i'll", "i'm", "in", "inc", "indeed",
    "interest", "into", "is", "isn", "it",  "it's", "its", "itself", "just", "keep", "know", "last", "latter",
    "latterly", "least", "less", "like", "ll", "ltd", "m", "made", "many", "me",
    "meanwhile", "might", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "me", "my", "myself", "name", "namely", "neither", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per",
    "please", "put", "rather", "re", "s", "same", "see", "several", "she", "she'll", "she's", "should", "show", "side",
    "since", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "t", "take", "ten", "than", "that", "that's", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "ve",
    "via", "want", "was", "wasn't", "we", "we'll", "well", "we're", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "you'll", "your", "you're", "yours", "yourself",
    "yourselves", "youv"]
	
	
# Remove stop words from the above list of words
def stop_word_remove(file):
	f = open(file)
	lines = map(lambda x: x.strip(), f.readlines())
	f.close()
	regex = "\\b|\\b".join(CUSTOMIZED_STOP_WORDS)
	lines = map(lambda x: re.sub("\\b" + regex + "\\b", "", x), lines)
	lines = map(lambda x: re.sub("'", "", x), lines)
	lines = map(lambda x: re.sub("\s\s+", " ", x), lines)
	f = open(file, "w")
	for line in lines:
		if line.strip():
			f.write(line.strip() + "\n")
	f.close()

	
# Use the Porter stemmer to stem a whole file and write to a new file
# Must tokenize words first, and characters out of the 128 ASCII range must be removed
def stem_file(in_file, out_file):
	f = open(in_file)
	lines = map(lambda x: x.strip(), f.readlines())
	f.close()
	f = open(out_file, "w")
	tokenizer = WordPunctTokenizer()
	stemmer = PorterStemmer()
	for line in lines:
		tok_line = tokenizer.tokenize(line)
		for i in range(len(tok_line)):
			spec = set()
			for c in tok_line[i]:
				if not ((47 < ord(c) < 58) or (64 < ord(c) < 91) or (96 < ord(c) < 123)):
					spec.add(c)
			for c in spec:
				tok_line[i] = tok_line[i].replace(c, '')
		tok_line = map(stemmer.stem, tok_line)
		f.write(' '.join(tok_line) + "\n")
	f.close()

# Run LDA on a file and write results to another file
# Sources: http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
# http://pythonhosted.org/lda/
def output_topics(read_file, write_file):
	f = open(read_file)
	lines = map(lambda x: x.strip(), f.readlines())
	f.close()
	f = open(write_file, "w")
	cv = CountVectorizer()
	arr = cv.fit_transform(lines)
	model = lda.LDA(n_topics=20, n_iter=2000, random_state=1)
	model.fit(arr)
	topic_word = model.topic_word_
	n_top_words = 8
	for i, topic_dist in enumerate(topic_word):
		topic_words = np.array(cv.vocabulary_.keys())[np.argsort(topic_dist)][:-n_top_words:-1]
		f.write('Topic {}: {}'.format(i, ' '.join(topic_words)))
		f.write("\n")
	f.close()
	
	
# Load the Stanford Parser through NLTK
def load_parser():
	jar = "C:/Users/User/Documents/JavaLibs/stanford-parser-full-2017-06-09/stanford-parser.jar"
	models = "C:/Users/User/Documents/JavaLibs/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar"
	p = StanfordDependencyParser(path_to_jar=jar, path_to_models_jar=models)
	return p
	
	
# Convert the output of NLTK's Stanford Parser to the Stanford format (required by the politeness classifier)
def convert_parse(nltk_parse):
	deps = []
	for d in nltk_parse:
		deps.append(d[1] + "(" + d[0][0] + ", " + d[2][0] + ")")
	return deps
	
	
# Parse a sentence (or sentences) into the format required for the politeness classifier
def dep_parse(parser, sentence):
	docs = []
	for s in sent_tokenize(sentence):
		info = {}
		info["text"] = s
		info["sentences"] = [s]
		result = parser.raw_parse(s)
		dep = result.next()
		parse = convert_parse(list(dep.triples()))
		info["parses"] = [parse]
		docs.append(info)
	return docs
	

# Pick 500 random lines from each gender-genre pair and parse
p = load_parser()
for file in filter(lambda x: "Lines" in x, os.listdir("SemiRawLines")):
	print file
	f = open("SemiRawLines/" + file)
	lines = f.readlines()
	f.close()
	f = open("ParseLines/" + file, "w")
	random.shuffle(lines)
	counter = 1
	for line in lines[:500]:
		if counter % 10 == 0: print counter
		for s in sent_tokenize(line.strip()):
			f.write(s + "\n")
			result = p.raw_parse(s)
			dep = result.next()
			parse = convert_parse(list(dep.triples()))
			for d in parse:
				f.write(d + "\n")
			f.write("$$$\n")
		counter += 1
	f.close()
	

#for file in os.listdir("Lines"):
#	clean_file("Lines/" + file, "SemiRawLines/" + file)
#	stop_word_remove("CleanLines/" + file)

#for file in os.listdir("CleanLines"):
#	output_topics("CleanLines/" + file, "LDATopics/" + file.replace("_Lines.txt", "_Topics20.txt"))
	
"""	
lines = movie_lines("movie_lines.txt")
titles = movie_titles_metadata("movie_titles_metadata.txt")
chars = movie_characters_metadata("movie_characters_metadata.txt")
gender_lines(lines, titles, chars, "All_Action_Male_Lines.txt", "m", "action")
gender_lines(lines, titles, chars, "All_Action_Female_Lines.txt", "f", "action")
gender_lines(lines, titles, chars, "All_Romance_Male_Lines.txt", "m", "romance")
gender_lines(lines, titles, chars, "All_Romance_Female_Lines.txt", "f", "romance")
gender_lines(lines, titles, chars, "All_Adventure_Male_Lines.txt", "m", "adventure")
gender_lines(lines, titles, chars, "All_Adventure_Female_Lines.txt", "f", "adventure")
gender_lines(lines, titles, chars, "All_Drama_Male_Lines.txt", "m", "drama")
gender_lines(lines, titles, chars, "All_Drama_Female_Lines.txt", "f", "drama")
"""
