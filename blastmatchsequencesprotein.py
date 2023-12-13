import os
import sys
import re
from filteringproteinfiles import PrintDictToFastaFile

'''
This code takes in the output from the blast file, extracts the sequences 
and matches them with the sequence headers in the protein fasta file. 
The output is stored in a dictionary and is then printed to an output file.

Blast file sequences look like:
Lipotes_vexillifer_XP_007465438.1_PREDICTED:_tyrosine-protein_phosphatase_non-receptor_type_substrate_1_isoform_X1
Sequence headers look like:
Lipotes_vexillifer_XP_007465438.1_PREDICTED:_tyrosine-protein_phosphatase_non-receptor_type_substrate_1_isoform_X1
'''

# Function to convert a fasta file to a dictionary
def convertfastatodict_simple(filename):
    # Open the fasta file for reading
    fi = open(filename, 'r')
    key = ''
    value = ''
    # Iterate through each line in the file
    for line in fi:
        line = line.strip()
        if line.startswith(">"):  # Check if the line is a header
            if key != '':
                fastadict[key] = value
            key = line[1:]
            value = ''  # Reset value for a new header
            continue
        else:
            value += line.strip()  # Append sequence to the dictionary

# Function to extract top hits from a blast file, filter out isoforms, and store them in a list
def tophitsfromblast_filtering(filename, hits_list):
    fi = open(filename, 'r')
    for line in fi:
        cols = line.split("\t")
        hit = cols[1]
        hits_list.append(hit)

if __name__ == '__main__':
    print("Code is running, don't worry!")
    fastadict = {}
    filtered_dict = {}
    hits_list = []

    # Get file paths from command line arguments
    fastafile = sys.argv[1]
    blastinput = sys.argv[2]
    blastseqoutput = sys.argv[3]

    # Convert fasta file to a dictionary
    convertfastatodict_simple(fastafile)

    # Extract top hits from blast file and filter out isoforms
    tophitsfromblast_filtering(blastinput, hits_list)

    # Remove duplicates from the hits list
    hits_set = set(hits_list)
    hits_list = list(hits_set)

    # Match hits with sequence headers and store in a new dictionary
    for item in hits_list:
        for key, val in fastadict.items():
            if item == key:
                filtered_dict[key] = val

    # Print the filtered dictionary to a fasta file
    PrintDictToFastaFile(filtered_dict, blastseqoutput)

    ##-- howtorun
    ##-- python3 scriptname.py 
    ##--python3 blastmatchsequencesprotein.py dataset/vertebrates_protein.faa human_vertebratesdb_e5.txt human_vertebratesdb_e5_seq.faa
