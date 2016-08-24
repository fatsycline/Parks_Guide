My goal is to make a program that reads through a file containing data on all our National Parks. There will be at least 3 search criteria: Park Name, State, Descriptions of the parks. The main page will be Ascii art of the Nat'l Parks emblem.

All the steps taken to create... 'THE NATIONAL PARK SEARCH ENGINE':

1. Skim the HTML of the Wikipedia page containing the information on parks and extract it from the file. I will do this by writing a pattern that looks for the table in the html and reads it row by row and then extracts the columns. 

2. Turn the extracted information into a variable by making it a list. I will also write it to a .tsv file so that I can organize the data. Part of the extraction is to remove the html tags from the text by stripping it.

3. Write a loop to extract the data that I'm searching by iterating each row and cleaning up the data, then saving it into a list 

4. Create a function that scans for matches in the list of parks and pulls up and returns a list of parks that match. There are flags to make it case insensitive. Using the regular expression (re) module to do the match.

5. Write a function that color codes the different type of data for the park and prints to the console.

6. Create a boolean loop to write the questions that promts the users the questions for them to enter an input that feeds into the park search function.

7. For each match from the search function, print it out using the color coding function.


Notes on areas I want to improve:

# improvement to do: when no matches from a description, recommend to try a different word
#   e.g. bison instead of buffalo
#   ex. bison instead of buffalo
# I need to figure out how to exit out when done. also maybe add a 'fun facts' section.
# I also want to be able to narrow down location to Midwest, Southwest, NE, NW, SW, or similar.
# I need to add an else: incase there is no national park in a state
# it would be great if people could narrow down their searches too, e.g. volcanoes in the nw
