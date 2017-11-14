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
	
output_lines(["TONY", "IRON MAN", "STEVE", "CAPTAIN AMERICA", "THOR"], "AvengersScript.txt", "Avengers_Male.txt")
output_lines(["PEPPER", "BLACK WIDOW", "NATASHA", "AGENT MARIA HILL"], "AvengersScript.txt", "Avengers_Female.txt")