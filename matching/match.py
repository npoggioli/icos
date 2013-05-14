# -*- coding: utf-8 -*-

#########################################
## DOCUMENT YOUR CODE USING DOCSTRINGS ##
#########################################

"""match.py: Demonstrate tools for linking messy data for ICOS Data Camp.

Provides a step by step demonstration of some basic tools for linking data
on contracts from the Department of Defense to lobbying contributions reported
on OpenSecrets.

"""

__author__ = "Russell J. Funk"
__date__ = "May 21, 2013"
__status__ = "Development"

#####################
## IMPORT PACKAGES ##
##################### 

# built in modules
import csv
import difflib

# third party modules

# custom modules
import preprocess

#############################################################################
## OPEN THE DOD CONTRACT DATA; LOOP THROUGH RECORDS TO PULL OUT FIRM NAMES ##
#############################################################################

print "reading DOD data..."

dod_firms = [] # make a list to store raw firm names and awards
dod_raw = [] # make a list for comparing raw to clean names

# open csv file and pull out "Firm" and "Award Amount" fields
with open("data/AwardsToExcel.csv", "rb") as f:
    dod_records = csv.DictReader(f, delimiter=",", quotechar='"')

    # add each record to our list
    for dod_record in dod_records:
        dod_firms.append([dod_record["Firm"], dod_record["Award Amount"]])
        dod_raw.append(dod_record["Firm"])
        
#####################################################################
## OPEN LOBBYING DATA; LOOP THROUGH RECORDS TO PULL OUT FIRM NAMES ##
#####################################################################

print "reading OS data..."

lob_firms = [] # make a list to store raw firm names and payments

# the raw file is missing a header; give it one
header = ["Client", "Sub", "Total", "Year", "Catcode"] 

# open csv file and pull out "Client" and "Total" fields
with open("data/lob_indus.txt", "rb") as f:
    lob_records = csv.DictReader(f, fieldnames=header, delimiter=",", 
                                 quotechar="|")
    
    # add each record to our list
    for lob_record in lob_records:
        lob_firms.append([lob_record["Client"], lob_record["Total"]])
                
################################
## CLEAN FIRM NAME CHARACTERS ##
################################

"""Clean firm name characters.

Using a simple function stored in a local module (preprocess), loop through 
each firm name in the DOD and OS data. Remove select punctuation, excessive
whitespace, convert to lowercase, and strip accents when possible. Note that
what is reasonable to "clean" depends on your context! 

"""

print "cleaning DOD firm name characters..."

# [i][0] means, for element i of the list, get item [0] (i.e., the firm name)
for i in range(len(dod_firms)):
    dod_firms[i][0] = preprocess.clean_firm_name(dod_firms[i][0])

print "cleaning OS firm name characters..."

for i in range(len(lob_firms)):
    lob_firms[i][0] = preprocess.clean_firm_name(lob_firms[i][0])

###############################################
## NORMALIZE FIRM NAMES IN DOD CONTRACT DATA ##
###############################################

"""Normalize firm name characters.

Using a simple function stored in a local module (preprocess), loop through 
each firm name in the DOD and OS data. Convert common abbreviations, 
misspellings, and other name variations to a standard form using a dictionary.
Again, what is reasonable to "normalize" depends on your context! 

"""

print "normalizing DOD firm name characters..."

for i in range(len(dod_firms)):
    dod_firms[i][0] = preprocess.normalize_firm_name(dod_firms[i][0])

print "normalizing OS firm name characters..."

for i in range(len(lob_firms)):
    lob_firms[i][0] = preprocess.normalize_firm_name(lob_firms[i][0])

#####################################################
## DEDUPLICATE FIRM NAMES WITHIN DOD CONTRACT DATA ##
#####################################################

"""Deduplicate the DOD firm list with itself.

Cleaning and normalization will enable us to group quite a few of the firm
names together already, but those methods only get around some problems. For
example, our script would not match "coherent technologies" and "coherent
technologies inc". Wouldn't it be nice to add a little fuzziness to the 
matching process? We can! Use a built in library called "difflib". This library
implements one of many, many algorithms available for string matching. It works
decently well and is bundled with python, which is good. But, it can be slow.
For more, see: http://en.wikipedia.org/wiki/String_metric  

The challenge is that we do not have a set of reference names that we can use
for deduplicating. If we have "coherent technologies", "coherent technologies 
inc", and "coherent technologie inc", how do we know which one in the "real"
name in which is a duplicate? We don't. What we'll do here is just make an 
arbitrary rule that says whatever variant appears first in the big list of 
names is our standard. We loop through each name in the list, see if there is a
good match that comes earlier in the list than the name we are considering. If
we find one, assign it to the earlier name. Because there might be multiple
duplicates for each name (as in our coherent technologies example) we'll need
to loop through the list multiple times, until no additional updates are made.

Note that most often, spelling mistakes and variations in names come
at the end, not the beginning of the string, especially in the two data sets
we're trying to merge. The difflib algorithm does not take this into account,
and as a result often suggests bad matches (e.g., "kansas state university" and
"arkansas state university" look very similar to the algorithm). We'll use a 
little function in our preprocess module called "get_matching_items" that only
allows difflib to match on strings that begin with exactly the same X letters
(as captured by the "num_letters" parameter). 

We could (and probably should) do the same deduplication for the OS data. But
that list of names is substantially longer and deduplication takes longer than
we have time for in this session. If you're looking for extra practice, try 
adapting the code below for the DOD data to the OS names for practice.

"""

print "deduplicating DOD firm names..."

while True:
    updates_made = False
    for i in range(len(dod_firms)):
        # pull out names up to and including i in the list
        search_firms = [s[0] for s in dod_firms[:i]]
        search_firms = preprocess.get_matching_items(name=dod_firms[i][0], 
                                                     num_letters=3, 
                                                     reference=search_firms)

        match = difflib.get_close_matches(word=dod_firms[i][0], 
                                  possibilities=search_firms, 
                                  n=1, 
                                  cutoff=0.90)
        if len(match) > 0 and match[0] != dod_firms[i][0]:
          print("deduplicate DOD---replacing %s with %s..." % (dod_firms[i][0],
                                                               match[0]))
          dod_firms[i][0] = match[0]
          updates_made = True
          
    if updates_made is False:
      break # exit the "while" loop if no updates were made

#######################################################################
## EXPORT RAW DOD NAMES TO CLEAN NAME CROSSWALK FOR FUTURE REFERENCE ##
#######################################################################

"""Save your work for the future. 

At this point, we have a nice list of raw name variants and associated 
standardized names. If you're going to do future work on these firms, such a 
list might come in handy! More importantly, it also helps us check to make sure
our code is working how we intend. Take a look at "results/dod_crosswalk.csv".

"""

print "building DOD firm name crosswalk for future referece and evaluation..."

dod_clean = [c[0] for c in dod_firms] # pull out names (exclude awards)
dod_crosswalk = zip(dod_raw, dod_clean)

with open("results/dod_crosswalk.csv", "wb") as f:
    csv_f = csv.writer(f, quoting=csv.QUOTE_ALL)
    csv_f.writerows(dod_crosswalk)

##################################################
## GROUP FIRM NAMES IN DOD DATA INTO DICTIONARY ##
##################################################

print "building a dictionary of DOD awards and contracts..."

clean_dod_firms = {}
for dod_firm in dod_firms:
    firm_name = dod_firm[0]
    firm_awards = int(dod_firm[1])
  
    # say the number of contracts equals the times the firm appears in the list
    if firm_name in clean_dod_firms:
        clean_dod_firms[firm_name]["awards"] += firm_awards
        clean_dod_firms[firm_name]["contracts"] += 1
    else:
        clean_dod_firms[firm_name] = {"awards": firm_awards, "contracts": 1}

###########################################################
## GROUP FIRM NAMES IN OPEN SECRETS DATA INTO DICTIONARY ##
###########################################################

print "building a dictionary of OS lobbying payments..."

clean_lob_firms = {}
for lob_firm in lob_firms:
    firm_name = lob_firm[0]
    
    # an entry in the OS data is missing, which causes an error
    try:
        firm_payments = int(lob_firm[1])
    except ValueError:
        firm_payments = 0
  
    if firm_name in clean_lob_firms:
        clean_lob_firms[firm_name] += firm_payments
    else:
        clean_lob_firms[firm_name] = firm_payments

#########################################
## MATCH DOD DATA TO LOBBYING PAYMENTS ##
#########################################

print "matching DOD data to lobbying payments..."

LEADING_CHARS = 3
MATCHES_WANTED = 1
MATCHING_THRESHOLD = 0.85

"""Tip: avoid "magic numbers" in your code.

Use constants (like those above) to make your code easier to read and enhance 
its reusability. Normally, you would put these kinds of constants (think of 
them as tuning parameters) at the top of your program so you can easily make 
adjustments and have all the knobs in one place.

What is more readable and flexible (when you come back in 6 months)?

difflib.get_close_matches(dod_firm, search_lob_firms, 1, 0.90)

difflib.get_close_matches(word=dod_firm, possibilities=search_lob_firms, 
                          n=1, cutoff=0.90)

difflib.get_close_matches(word=dod_firm, possibilities=search_lob_firms, 
                          n=MATCHES_WANTED, cutoff=MATCHING_THRESHOLD)

"""

results = [] # a list to store our results

for dod_firm in clean_dod_firms.keys():
    search_lob_firms = preprocess.get_matching_items(dod_firm, LEADING_CHARS, 
                                                     clean_lob_firms)
    
    match = difflib.get_close_matches(word=dod_firm, 
                                      possibilities=search_lob_firms, 
                                      n=MATCHES_WANTED, 
                                      cutoff=MATCHING_THRESHOLD)

    if len(match) > 0:
        lob_firm = match[0]
        lob_payments = clean_lob_firms[match[0]]
    else:
        lob_firm = "" # if we don't have an OS match, use an empty string
        lob_payments = 0 

    # fill up our list of results 
    results.append([dod_firm, 
                   lob_firm, 
                   clean_dod_firms[dod_firm]["awards"],
                   clean_dod_firms[dod_firm]["contracts"],
                   lob_payments])

######################################
## EXPORT RESULTS FOR DATA ANALYSIS ##
######################################

print "exporting results..."

with open("results/drone_data.csv", "wb") as f:
    csv_f = csv.writer(f, quoting=csv.QUOTE_ALL)
    csv_f.writerow(["dod_firm", "lob_firm", "dod_awards", "dod_contracts", 
                    "lob_payments"]) # write a header row
    csv_f.writerows(results)