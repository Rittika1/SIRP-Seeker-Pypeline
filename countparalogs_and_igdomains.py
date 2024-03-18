####---- this code takes in a fasta file and counts number of occurences of one species.

import sys

# Get the input file name from the command line arguments
inputfile = sys.argv[1]

# Open the input file for reading
inf = open(inputfile, 'r')

# Initialize an empty dictionary to store the counts of each species
countsdict = {}

# Iterate through each line in the input file
for line in inf:
    # Check if the line starts with '>', indicating a new sequence header
    if line.startswith(">"):
        # Split the line based on the underscore character
        SplitLine = line.split("_")
        # Construct the species name by combining the first two parts of the split line
        speciesname = SplitLine[0][1:] + "_" + SplitLine[1].rstrip()
        # Check if the species name is already in the dictionary
        if speciesname in countsdict.keys():
            # If so, increment the count for that species
            countsdict[speciesname] += 1
        else:
            # Otherwise, add the species to the dictionary with a count of 1
            countsdict[speciesname] = 1

# Iterate through the items in the counts dictionary
for key, val in countsdict.items():
    # Print the species name and its count, separated by a tab character
    print(key, "\t", val)


##--usage
##--python3 SIRP-Seeker-Pypeline/countparalogs_and_igdomains.py Ig-domains/human-sirpa_hitdata_Igdomains_deduped.faa > Ig-domains/igdomain-count/human-igdomaincount.txt
##--python3 SIRP-Seeker-Pypeline/countparalogs_and_igdomains.py Ig-domains/cattle-sirpa_hitdata_Igdomains_deduped.faa > Ig-domains/igdomain-count/cattle-igdomaincount.txt
##--python3 SIRP-Seeker-Pypeline/countparalogs_and_igdomains.py Ig-domains/chicken-sirpa_hitdata_Igdomains_deduped.faa > Ig-domains/igdomain-count/chicken-igdomaincount.txt
##--python3 SIRP-Seeker-Pypeline/countparalogs_and_igdomains.py Ig-domains/trimmed-aliview/human-sirpa_hitdata_aligned_trimmed_merged.faa > paralogs/human-sirp-paralogs.txt
##--python3 SIRP-Seeker-Pypeline/countparalogs_and_igdomains.py Ig-domains/trimmed-aliview/cattle-sirpa_hitdata_aligned_trimmed_merged.faa > paralogs/cattle-sirp-paralogs.txt   
##--python3 SIRP-Seeker-Pypeline/countparalogs_and_igdomains.py Ig-domains/trimmed-aliview/chicken-sirpa_hitdata_aligned_trimmed_merged.faa > paralogs/chicken-sirp-paralogs.txt