
# use curses library to draw the ascii art
# improvement to do: when no matches from a description, recommend to try a different word
#   e.g. bison instead of buffalo
#   ex. bison instead of buffalo
# I need to figure out how to exit out when done. also maybe add a 'fun facts' section.
# I also want to be able to narrow down location to Midwest, Southwest, NE, NW, SW, or similar.
# I need to add an else: incase there is no national park in a state
# it would be great if people could narrow down their searches too, e.g. volcanoes in the nw
 

# ... urlb2 is a url fetching modul
# ... A regular expression (or RE) specifies a set of strings that matches it; 
# ... ... the functions in this module let you check if a particular string matches a given regular 
# ... ... expression (or if a given regular expression matches a particular string, which comes down to the same thing).
import urllib2
import re
import time
import sys
import json

# the wikipedia page I pulled the information from (the nat'l parks server was too slow)
body = urllib2.urlopen('https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States').read()

# ... re.compile is how i matched the pattern of the table in the doc so we can search it
# ... ... and the re.DOTALL flag helps with matching new lines in the table.
#pattern = re.compile(r'<tr>\s*<th[^>]*>\s*(.*?)</th>.*?</tr>', flags=re.DOTALL)
pattern = re.compile(r'<tr>' + (r'\s*<t[hd][^>]*>(.*?)</t[hd]>'*7) + '.*?</tr>', flags=re.DOTALL)

# ... this is removing all the html in the top line and second line is tabs and new lines.
def strip_html(s):
	s = re.sub(r'<[^>]*>', '', s)
	s = re.sub(r'[\n\t\r ]+', ' ', s)
	return s

# ... returns patterns by scanning left to right in a string as a list of strings and returning results as tuples. non duplicates.
# ... I skipped the first row because it's all headers. 
table_rows = pattern.findall(body)[1:]
parks = [
	(
		strip_html(name), 
		strip_html(location), 
		strip_html(date_established), 
		strip_html(description)
	)
	for (name, photo, location, date_established, area, recreation_visitors, description) in table_rows
	]
# ... this is the function that scans for matches in data and pulls up / matches the correct information
def find_parks(name_query=None, location_query=None, description_query=None):
	match_parks = parks
	if name_query is not None:
		p = re.compile(re.escape(name_query), flags=re.IGNORECASE)
		match_parks = [
			(name, location, date_established, description)
			for (name, location, date_established, description) in match_parks
			if p.search(name)
		]
	if location_query is not None:
		p = re.compile(re.escape(location_query), flags=re.IGNORECASE)
		match_parks = [
			(name, location, date_established, description)
			for (name, location, date_established, description) in match_parks
			if p.search(location)
		]
	if description_query is not None:
		p = re.compile(re.escape(description_query), flags=re.IGNORECASE)
		match_parks = [
			(name, location, date_established, description)
			for (name, location, date_established, description) in match_parks
			if p.search(description)
		]
	return match_parks


# for name, location, date_established, description in parks:
#     print '%s %s %s %s' % (name, location, date_established, description)
# a tstring format ('%s\t%s..' % (none, none,...)) because it's cleaner than combining strings with +s
def create_parks_doc(file_name):
	with open (file_name, mode = 'w') as my_file:
		for name, location, date_established, description in parks:
			my_file.write('%s\t%s\t%s\t%s\n' % (name, location, date_established, description))

create_parks_doc("natl_parks.tsv")


def print_parks(match_parks):
	for name, location, date_established, description in match_parks:
		# see http://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
	    print '\033[0;32m%s\033[0m \033[0;33m%s\033[0m %s %s' % (name, location, date_established, description)


def export():
	parks_ser = [
		{
			'name': name,
			'location': location,
			'date_established': date_established,
			'description': description
		}
		for name, location, date_established, description in parks
	]
	print json.dumps(parks_ser, sort_keys=True, indent=4, separators=(',', ': '))


def main():
	args = sys.argv[1:]
	if 1 == len(args) and '--export' == args[0]:
		export()
		return

	# print the Ascii art
	with open('parks_ascii_art.txt', 'r') as f:
		ascii_art = f.read()
	for line in ascii_art.split('\n'):
		print line
		time.sleep(0.1)
	while True:
		q = raw_input('Search parks by name, state, or description: ')
		if 'name' == q or q.startswith('n'):
			name = raw_input('Enter the name of the Nat\'l Park you want to search ')
			print_parks(find_parks(name_query=name))
		elif 'location' == q or q.startswith('l') or q.startswith('s'):
			state = raw_input('Which state do you want to search? ')
			print_parks(find_parks(location_query=state))
		elif 'description' == q or q.startswith('d'):
			about = raw_input('Which feature do you want to search? \n e.g. Mountains, Desert, Volcanoe ')
			print_parks(find_parks(description_query=about))


if '__main__' == __name__:
	main()

