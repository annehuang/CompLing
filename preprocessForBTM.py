from nltk.stem.snowball import SnowballStemmer
import nltk
import re

# http://www.nltk.org/howto/stem.html

# this is the list of stop words from SK-Learn
# I am taking out a few: "very", "first"
#https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/feature_extraction/stop_words.py
# http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/
# "first" comes on in some topics from existing work
# http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf
# take out could perhaps may
# add hes shes youv isn wasnt youll id
CUSTOMIZED_STOP_WORDS = [
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con","couldnt",
    "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hes", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "id", "ie", "if", "i'm", "in", "inc", "indeed",
    "interest", "into", "is", "isn", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "me", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "shes", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "via", "was", "wasnt", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "youll", "your", "you'r", "yours", "yourself",
    "yourselves", "youv"]

def preprocessForBTM(filename):
    stemmer = SnowballStemmer("english")
    ret = ""
    f = open(filename + ".txt", "r").readlines()
    for line in f:
        line = re.sub(r'\d', '', line)
        line = line.lower()
        line = line.replace(".", "")
        line = line.replace(",", "")
        line = line.replace("'", "")
        line = line.replace("?", "")
        line = line.replace("  ", " ")
        line = line.strip(" ")
        line = line.split(" ")
        for word in line:
            if word != " ":
                try:
                    if nltk.pos_tag([word])[0][1] != "JJ": # http://www.nltk.org/book/ch05.html https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/
                    # empathy paper
                        if word not in CUSTOMIZED_STOP_WORDS:
                            word = stemmer.stem(word)
                            if word not in CUSTOMIZED_STOP_WORDS:
                                ret += word
                                ret += " "
                except:
                    continue
    f2 = open(filename + "cleaned.txt", "w")
    f2.write(ret)
    f2.close()

def romanceMovies():
    SCRIPTS = ["PrideFemaleOutput", "PrideMaleOutput", "SexCityFemaleOutput", "SexCityMaleOutput", "TitanicFemaleOutput", "TitanicMaleOutput", "YouveGotFemaleOutput", "YouveGotMaleOutput"]
    batch(SCRIPTS)
    
def action():
    SCRIPTS = ["AmericanSniper_ChrisKyle", "Avengers_Male", "BourneUltimatum_JasonBourne", "maleItalianOutput", "AmericanSniper_TayaKyle", "Avengers_Female", "BourneUltimatum_NickyParsons", "femaleItalianOutput"]
    batch(SCRIPTS)
    
def batch(scripts):
    for script in scripts:
        preprocessForBTM(script)        
