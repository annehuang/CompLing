"""
Modified from Danescu-Niculescu-Mizil et al.'s classifier (https://github.com/sudhof/politeness).
The main function has been modified to read our files, and extra functions have been added to open/parse files.
Requires older versions of numpy, scipy, and scikit-learn.
"""


import sys
import os
import cPickle

"""
This file provides an interface to 
a pre-trained politeness SVM. 
"""

#####
# Ensure the proper python dependencies exist

try:
    import numpy as np
except:
    sys.stderr.write("Package not found: Politeness model requires python package numpy\n")
    sys.exit(2)

try:
    import scipy
    from scipy.sparse import csr_matrix
except:
    sys.stderr.write("Package not found: Politeness model requires python package scipy\n")
    sys.exit(2)

try:
    import sklearn
except:
    sys.stderr.write("Package not found: Politeness model requires python package scikit-learn\n")
    sys.exit(2)

try:
    import nltk
except:
    sys.stderr.write("Package not found: Politeness model requires python package nltk\n")
    sys.exit(2)

####
# Check versions for sklearn, scipy, numpy, nltk
# Don't error out, just notify

packages2versions = [("scikit-learn", sklearn, "0.15.1"), ("numpy", np, "1.9.0"), ("nltk", nltk, "3.0.0"), ("scipy", scipy, "0.12.0")]

for name, package, expected_v in packages2versions:
    if package.__version__ < expected_v:
        sys.stderr.write("Warning: package '%s', expected version >= %s, detected %s. Code functionality not guaranteed.\n" % (name, expected_v, package.__version__))


####

from features.vectorizer import PolitenessFeatureVectorizer


####
# Serialized model filename

MODEL_FILENAME = os.path.join(os.path.split(__file__)[0], 'politeness-svm.p')

####
# Load model, initialize vectorizer

clf = cPickle.load(open(MODEL_FILENAME))
vectorizer = PolitenessFeatureVectorizer()

def score(request):
    """
    :param request - The request document to score
    :type request - dict with 'sentences' and 'parses' field
        sample (taken from test_documents.py)--
        {
            'sentences': [
                "Have you found the answer for your question?", 
                "If yes would you please share it?"
            ],
            'parses': [
                ["csubj(found-3, Have-1)", "dobj(Have-1, you-2)", "root(ROOT-0, found-3)", "det(answer-5, the-4)", "dobj(found-3, answer-5)", "poss(question-8, your-7)", "prep_for(found-3, question-8)"], 
                ["prep_if(would-3, yes-2)", "root(ROOT-0, would-3)", "nsubj(would-3, you-4)", "ccomp(would-3, please-5)", "nsubj(it-7, share-6)", "xcomp(please-5, it-7)"]
            ]
        } 

    returns class probabilities as a dict
        {
            'polite': float, 
            'impolite': float
        }
    """
    # vectorizer returns {feature-name: value} dict
    features = vectorizer.features(request)
    fv = [features[f] for f in sorted(features.iterkeys())]
    # Single-row sparse matrix
    X = csr_matrix(np.asarray([fv]))
    probs = clf.predict_proba(X)
    # Massage return format
    probs = {"polite": probs[0][1], "impolite": probs[0][0]}
    return probs



if __name__ == "__main__":

	"""
    

    from test_documents import TEST_DOCUMENTS

    for doc in TEST_DOCUMENTS:

        probs = score(doc)

        print "===================="
        print "Text: ", doc['text']
        print "\tP(polite) = %.3f" % probs['polite']
        print "\tP(impolite) = %.3f" % probs['impolite']
        print "\n"
	"""
	
	from features.politeness_strategies import check_elems_for_strategy, initial_polar, aux_polar


	def check_is_request(document):
		"""
		Heuristic to determine whether a document
		looks like a request

		:param document- pre-processed document
			that might be a request
		:type document- dict with fields 
			'sentences' and 'parses', as
			in other parts of the system
		"""
		for sentence, parse in zip(document['sentences'], document['parses']):
			if "?" in sentence:
				return True
			if check_elems_for_strategy(parse, initial_polar) or check_elems_for_strategy(parse, aux_polar):
				return True
		return False
		
		
	# Read the parser output from a file
	def read_parse(file):
		f = open(file)
		lines = f.readlines()
		f.close()
		docs = []
		thisdoc = {}
		thisparse = []
		start = True
		for line in lines:
			if start:
				thisdoc["text"] = line.strip()
				thisdoc["sentences"] = [line.strip()]
				thisdoc["parses"] = []
				start = False
			elif line.strip() == "$$$":
				thisdoc["parses"].append(thisparse)
				docs.append(thisdoc)
				thisdoc = {}
				thisparse = []
				start = True
			else:
				thisparse.append(line.strip())
		return docs
		
		
	# Read the parser output from a file, run their simple function to check if sentence is a request,
	# and run the politeness classifier on the requests only. Write output to a file.
	def parse_polite(in_file, out_file):
		docs = read_parse(in_file)
		f = open(out_file, "w")
		for doc in docs:
			if check_is_request(doc):
				f.write(doc["text"] + "\n")
				probs = score(doc)
				f.write(str(probs['polite']) + "\n")
				f.write(str(probs['impolite']) + "\n")
		f.close()
		
		
	# Get stats of the politeness output
	def polite_stats(file):
		f = open(file)
		lines = f.readlines()
		f.close()
		n = len(lines) / 3
		polite = map(float, lines[1::3])
		impolite = map(float, lines[2::3])
		#avgpolite = sum(map(float, lines[1::3]))/n
		#avgimpolite = sum(map(float, lines[2::3]))/n
		return n, polite, impolite
		
		
	# Run standard t-test on two sets of scores (male vs. female in one genre)
	def politeness_ttest(scores1, scores2):
		return scipy.stats.ttest_ind(scores1, scores2)
		
			
	
	D = "C:/Users/User/Documents/UIC/SNLP/cornell_movie_dialogs_corpus/cornell movie-dialogs corpus/"
	files = ["All_Action_", "All_Adventure_", "All_Drama_", "All_Romance_"]
	for file in files:
		print file
		#parse_polite(D + "ParseLines/" + file + "Male, D + "Politeness/" + file)
		malen, malepolite, maleimpolite = polite_stats(D + "Politeness/" + file + "Male_Lines.txt")
		femalen, femalepolite, femaleimpolite = polite_stats(D + "Politeness/" + file + "Female_Lines.txt")
		print malen, femalen
		print politeness_ttest(malepolite, femalepolite)
		print politeness_ttest(maleimpolite, femaleimpolite)
		print "====================="

