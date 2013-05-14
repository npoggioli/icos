# -*- coding: utf-8 -*-

"""preprocess.py: Functions for preprocessing firm names for ICOS Data Camp."""

__author__ = "Russell J. Funk"
__date__ = "May 21, 2013"
__status__ = "Development"

# built in modules
import re
import unicodedata

# third party modules

# custom modules

def clean_firm_name(name):
    """Convert a firm name to ASCII characters and strip punctuation."""
    
    # convert accented and other characters to base form
    name = name.decode("iso-8859-1")
    name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore")
    
    # convert entire name to lowercase
    name = name.lower()
  
    # substitute characters with spaces or eliminate them
    name = re.sub(r"_|-|\+|/|\\", " ", name)
    name = re.sub(r"""\.|,|;|:|\(|\)|\[|\]|\{|\}|"|'""", "", name)  

    # replace "&" with " and "
    name = name.replace("&"," and ")
  
    # remove "the" from the beginning of names
    name = name.split()  
    if len(name) > 1 and name[0] == "the":
        name = name[1:]

    # join the string back together
    name = " ".join(name)
  
    # return the result
    return name

firm_abbrs = {
    "cnty": "county",
    "adv": "advanced",
    "aktiengesellschaft": "ag",
    "assoc": "associates",
    "assn": "association",
    "attys": "attorneys",
    "ctr": "center",
    "centre": "center",
    "coll": "college",
    "coltd": "co ltd",
    "company": "co",
    "corporation": "corp",
    "govt": "government",
    "grp": "group",
    "incorporated": "inc",
    "incorporation": "inc",
    "inst": "institute",
    "intl": "international",
    "jr": "junior",
    "kabushiki kaisha": "kk",
    "labs": "laboratories",
    "lab": "laboratory",
    "limited": "ltd",
    "natl": "national",
    "res": "research",
    "saint": "st",
    "sci": "science",
    "societe anonyme": "sa",
    "stt": "state",
    "sys": "systems",
    "syst": "systems",
    "technol": "technology",
    "univ": "university"
}

def normalize_firm_name(name):
    """Normalize a firm name using standard abbreviations."""
    name = name.split()
    name_norm = []
    for abbr in name:
        if abbr in firm_abbrs:
            name_norm.append(firm_abbrs[abbr])
        else: 
            name_norm.append(abbr)
    name_norm = " ".join(name_norm)
    return name_norm
    
def get_matching_items(name, num_letters, reference):
    """return a list of item matching first letters of a name."""
    filtered_items = []
    for item in reference:
        if item[0:num_letters] == name[0:num_letters]: 
            filtered_items.append(item)
    return filtered_items