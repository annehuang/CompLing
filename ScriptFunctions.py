# Natawut Monaikul, Anne Huang
# CS 521 Project
# Fall 2017

import re

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
			if line == "\n":
				append = False
				final_lines.append(' '.join(this_line))
				this_line = []
			elif "(" not in line:
				clean_line = re.sub("<.+>", "", line)
				clean_line = re.sub("\s\s+", " ", clean_line)
				clean_line = clean_line.strip()
				this_line.append(clean_line)
	return final_lines
	
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
	
#output_lines(["TONY", "IRON MAN", "STEVE", "CAPTAIN AMERICA", "THOR"], "AvengersScript.txt", "Avengers_Male.txt")
#output_lines(["PEPPER", "BLACK WIDOW", "NATASHA", "AGENT MARIA HILL"], "AvengersScript.txt", "Avengers_Female.txt")

def setCharactersCruelIntentions():
        F_CRUEL = ['RACHEL', 'MRS. CALDWELL', 'CECILE', 'KATHRYN', 'AUNT HELEN', 'ANNETTE', 'AUNT HELEN', 'AUNT HELEN', 'ANNETTE']
        M_CRUEL = ['DR. GREENBAUM', 'SEBASTIAN', 'RONALD', 'BLAINE', 'GREG', 'MRS. SUGARMAN']

def output_Clueless():
        FEMALE_CLUELESS = ['CHER V.O.', 'CHER', 'DIONNE', 'TAI', 'AMBER', 'LUCY', 'MISS GEIST', 'MISS STOEGER', 'HEATHER', 'SUMMER']
        MALE_CLUELESS = ['JOSH', 'MURRAY', 'TRAVIS', 'ELTON', 'MEL', 'MR. HALL', 'CHRISTIAN', 'PAROUDASM', 'PRINCIPAL', 'DMV TESTER', 'LAWRENCE', 'COLLEGE GUY', 'ROBBER', 'LOGAN', 'MINISTER', 'STUDENT', 'BARTENDER']
        CLUELESS = 'Clueless.txt'
        output_lines(FEMALE_CLUELESS, CLUELESS, "femaleCluelessOutput.txt")

def output_JaneEyre():
        MALE = ['ROCHESTER', 'ST JOHN', 'JOHN REED', 'LORD INGRAM']
        FEMALE = ['ADELE', 'GRACE', 'BLANCHE', 'LADY INGRAM', 'MISS SCATCHERD', 'HANNAH', 'JANE', 'MARY', 'DIANA', 'BESSIE', 'MISS ABBOT', 'MISS TEMPLE']
        JANE_EYRE = 'JaneEyre.txt'
        output_lines(FEMALE, JANE_EYRE, 'JaneEyreFemaleOutput.txt')

def output_PrettyWoman():
        MALE = ['EDWARD', 'LANDLORD', 'DAVID', 'LANDLORD', 'INVESTMENT BANKER 1', 'INVESTMENT BANKER 2', 'INVESTMENT BANKER 3', 'STUCKEY', 'BUTLER', 'A MAN', 'THE MAN']
        FEMALE = ['VIVIAN', 'ELIZABETH']
        PRETTYWOMAN = 'PrettyWoman.txt'
        output_lines(FEMALE, PRETTYWOMAN, 'PrettyWomanFemaleOutput.txt') 
        output_lines(MALE, PRETTYWOMAN, 'PrettyWomanMaleOutput.txt')

# 10 Things I Hate About You, Pride and Prejudice, Titanic, Youve Got Mail
def output_RestRomance():
        MALE_10 = ['RIDER', 'JOEY', 'BOY', 'PATRICK', 'MICHAEL', 'DEREK', 'CAMERON']
        FEMALE_10 = ['KAT', 'SHARON', 'BIANCA', 'CHASTITY', 'GIRL', 'MISS PERKY']
        TENTHINGS = '10Things.txt'
        output_lines(FEMALE_10, TENTHINGS, '10ThingsFOutput.txt') 
        output_lines(MALE_10, TENTHINGS, '10MaleOutput.txt')
        
        MALE_PRIDE = ['DARCY', 'MR BENNET', 'MR COLINS', 'MR BINGLEY', 'BINGLEY']
        FEMALE_PRIDE = ['ELIZABETH', 'JANE', 'MRS GARDINER', 'MRS BENNET', 'LYDIA', 'KITTY', 'CHARLOTTE', 'MARY', 'CAROLINE']
        PRIDE = 'PrideAndPrejudice.txt'
        output_lines(FEMALE_PRIDE, PRIDE, 'PrideFemaleOutput.txt') 
        output_lines(MALE_PRIDE, PRIDE, 'PrideMaleOutput.txt')
        
        M_TITANIC = ['ANATOLY', 'JACK', 'LOVETT', 'BODINE', 'LOVETT', 'CAL', 'MAN', 'FABRIZIO', 'JACK', 'FABRIZIO/JACK', 'ISMAY', 'LOVEJOY', 'MURDOCH']
        F_TITANIC = ['ROSE', 'RUTH', 'MOLLY']
        TITANIC = 'Titanic.txt'
        output_lines(F_TITANIC, TITANIC, 'TitanicFemaleOutput.txt') 
        output_lines(M_TITANIC, TITANIC, 'TitanicMaleOutput.txt')
        
        M_YOUVEGOT = ['FRANK', 'JOE', 'GEORGE', 'KEVIN', 'JOE']
        F_YOUVEGOT = ['KATHLEEN', 'PATRICIA', 'CHRISTINA']
        YOUVEGOT = 'YouveGotMail.txt'
        output_lines(F_YOUVEGOT, YOUVEGOT, 'YouveGotFemaleOutput.txt') 
        output_lines(M_YOUVEGOT, YOUVEGOT, 'YouveGotMaleOutput.txt')

        M_SEXANDCITY = ['BIG', 'AIDEN', 'STEVE']
        F_SEXANDCITY = ['CARRIE', 'SAMANTHA', 'MIRANDA', 'CHARLOTTE']
        SEXANDCITY = 'SexAndCity.txt'
        output_lines(F_SEXANDCITY, SEXANDCITY, 'SexCityFemaleOutput.txt') 
        output_lines(M_SEXANDCITY, SEXANDCITY, 'SexCityMaleOutput.txt')
        
def output_ItalianJob():
        ITALIAN_JOB = "italianjob.txt"
        MALE_CHARS = ['CHARLIE', 'BULLY', 'LYLE', 'STEVE', 'JOHN BRIDGER', 'HANDSOME ROB', 'RICHARD', 'VALET', 'DETECTIVE', 'MAKOV', 'FURIOUS DRIVER']
        FEMALE_CHARS = ['CHRISTINA', 'KAREN', 'STELLA']
        output_lines(MALE_CHARS, ITALIAN_JOB, "maleItalianOutput.txt")
        output_lines(FEMALE_CHARS, ITALIAN_JOB, "femaleItalianOutput.txt")
