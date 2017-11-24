from nltk.stem.snowball import SnowballStemmer
import re
# http://www.nltk.org/howto/stem.html

# this is the list of stop words from SK-Learn
# I am taking out a few: "you" (as in thank you), "very", "first"
#https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/feature_extraction/stop_words.py
# http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/
# "first" comes on in some topics from existing work
# http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf
CUSTOMIZED_STOP_WORDS = [
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "i'm", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "me", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "you'r", "yours", "yourself",
    "yourselves"]

def preprocessForBTM(filename):
    stemmer = SnowballStemmer("english")
    ret = ""
    f = open(filename + ".txt", "r").readlines()
    for line in f:
        line = re.sub(r'\d', '', line)
        line = line.lower()
        line = line.replace(".", " ")
        line = line.replace(",", " ")
        line = line.replace("'", " ")
        line = line.replace("?", " ")
        line = line.split(" ")
        for word in line:
            if word not in CUSTOMIZED_STOP_WORDS:
                word = stemmer.stem(word)
                if word not in CUSTOMIZED_STOP_WORDS:
                    ret += word
                    ret += " "
    f2 = open(filename + "cleaned.txt", "w")
    f2.write(ret)
    f2.close()

def main():
    SCRIPTS = ["Avengers_Male", "BourneUltimatum_JasonBourne", "maleItalianOutput", "AmericanSniper_TayaKyle", "Avengers_Female", "BourneUltimatum_NickyParsons", "femaleItalianOutput"]
    #preprocessForBTM("AmericanSniper_ChrisKyle")
    for script in SCRIPTS:
        preprocessForBTM(script)
