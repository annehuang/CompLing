import re, os
from nltk.tokenize import word_tokenize, WordPunctTokenizer
from nltk.stem.porter import PorterStemmer

# Get all lines spoken by the given set of names
# "lines" is f.readlines() from a file f
# "names" is all the (exact) names that should be included -- if I want all of Jason Bourne's lines, I might do ["JASON", "JASON BOURNE", "BOURNE"]
# return value is all lines of all names specified in a list, where each element is a whole line in the script
def extract_lines(lines, names):
	final_lines = []
	names_joined = '|'.join(names)
	name_regex = "<b>\s+(" + names_joined + ")\n"
	append = False
	this_line = []
	for line in lines:
		if re.match(name_regex, line):
			append = True
		elif append:
			if re.match("s*\n", line):
				append = False
				final_lines.append(' '.join(this_line))
				this_line = []
			else:
				clean_line = re.sub("<.+>|\(.+\)", "", line)
				clean_line = re.sub("\s\s+", " ", clean_line)
				clean_line = clean_line.strip()
				this_line.append(clean_line)
	return final_lines
	

# Open a file and read in the lines to run 'extract_lines' on it.
# "names" is all the exact names that should be included (read above)
# "read_file" is the script file to read in
# "write_file" is where the cleaned lines should be written to
def output_lines(names, read_file, write_file):
	f = open(read_file)
	lines = f.readlines()
	f.close()
	final_lines = extract_lines(lines, names)
	f = open(write_file, "w")
	f.write("\n".join(final_lines))
	f.close()
	
	
# Combine lines from two files into a single file
def combine_lines(in_file1, in_file2, out_file):
	f = open(in_file1)
	lines1 = f.readlines()
	f.close()
	f = open(in_file2)
	lines2 = f.readlines()
	f.close()
	f = open(out_file, "w")
	for line in lines1:
		f.write(line)
	for line in lines2:
		f.write(line)
	f.close()
	

# Tokenize all lines in a file and write to another file
def tokenize_file(in_file, out_file):
	f = open(in_file)
	lines = map(lambda x: x.strip(), f.readlines())
	f.close()
	f = open(out_file, "w")
	tokenizer = WordPunctTokenizer()
	for line in lines:
		tok_line = tokenizer.tokenize(line)
		for i in range(len(tok_line)):
			spec = set()
			for c in tok_line[i]:
				if not ((47 < ord(c) < 58) or (64 < ord(c) < 91) or (96 < ord(c) < 123)):
					spec.add(c)
			for c in spec:
				tok_line[i] = tok_line[i].replace(c, '')
		f.write(' '.join(tok_line) + "\n")
	f.close()

	
# Tokenize and stem all lines in a file and write to another file
def tokenize_and_stem_file(in_file, out_file):
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
	
	
# 'tokenize_file' for a whole directory
def tokenize_files(in_dir, out_dir):
	files = os.listdir(in_dir)
	for file in files:
		tokenize_file(in_dir + "/" + file, out_dir + "/" + file)
	

# 'tokenize_and_stem_file' for a whole directory	
def tokenize_and_stem_files(in_dir, out_dir):
	files = os.listdir(in_dir)
	for file in files:
		tokenize_and_stem_file(in_dir + "/" + file, out_dir + "/" + file)

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
    "bottom", "but", "by", "call", "co", "con","couldnt",
    "cry", "de", "describe", "detail", "did", "didn't", "do", "don't", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "he'll", "he's", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "id", "ie", "if", "i'll", "i'm", "in", "inc", "indeed",
    "interest", "into", "is", "isn", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ll", "ltd", "m", "made", "many", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "me", "my", "myself", "name", "namely", "neither", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per",
    "please", "put", "rather", "re", "s", "same", "several", "she", "she'll", "she's", "should", "show", "side",
    "since", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "t", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "ve",
    "via", "was", "wasnt", "we", "we'll", "well", "we're", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "you'll", "your", "you're", "yours", "yourself",
    "yourselves", "youv"]
	
	
# Remove all stop words from a file using the above list
def stop_word_remove(file):
	f = open(file)
	lines = map(lambda x: x.lower(), f.readlines())
	f.close()
	regex = "\\b|\\b".join(CUSTOMIZED_STOP_WORDS)
	lines = map(lambda x: re.sub("\\b" + regex + "\\b", "", x), lines)
	f = open(file, "w")
	for line in lines:
		f.write(line)
	f.close()
	
#output_lines(["ALFRED", "WAYNE", "GORDON", "BLAKE", "FATHER REILLY", "MARK", "STRYVER", "BANE", "THUG 1", "THUG 2", "BLAKE \(CONT'D\)", "FOX", "ALFRED \(CONT'D\)", "ALLEN", "FOLEY", "DAGGETT", "BATMAN"], "Scripts/DarkKnightRisesScript.txt", "MaleLines/DarkKnightRises_Male.txt")
#output_lines(["SELINA", "JEN", "JEN \(O\.S\.\)", "MIRANDA", "MIRANDA \(O\.S\.\)", "MIRANDA \(V\.O\.\)", "CATWOMAN", "CATWOMAN \(O\.S\.\)", "SELINA \(CONT'D\)", "TALIA"], "Scripts/DarkKnightRisesScript.txt", "FemaleLines/DarkKnightRises_Female.txt")
#combine_lines("MaleLines/DarkKnightRises_Male.txt", "FemaleLines/DarkKnightRises_Female.txt", "AllLines/DarkKnightRises_All.txt")

#tokenize_files("MaleLines", "MaleLinesModified")
#tokenize_files("FemaleLines", "FemaleLinesModified")
#tokenize_files("AllLines", "AllLinesModified")

for file in os.listdir("MaleLinesModified"):
	stop_word_remove("MaleLinesModified/" + file)
	combine_lines("All_Male_Lines_Tokenized.txt", "MaleLinesModified/" + file, "All_Male_Lines_Tokenized.txt")
