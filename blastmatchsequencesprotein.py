import os
import sys
import re
from filteringproteinfiles import PrintDictToFastaFile

'''
This code takes in the output from the blast file, extracts the sequences and matches them with the sequence headers in the protein fasta file. The output is stored in a dicitonary, and is then printed to an output file.
blast file sequences look like:
Lipotes_vexillifer_XP_007465438.1_PREDICTED:_tyrosine-protein_phosphatase_non-receptor_type_substrate_1_isoform_X1
sequence headers look like:
Lipotes_vexillifer_XP_007465438.1_PREDICTED:_tyrosine-protein_phosphatase_non-receptor_type_substrate_1_isoform_X1
'''

 ##-- replace the . with _ abd feed fast file in mafft
def convertfastatodict_simple(filename):
    # print ("Got the function we want!")
    fi = open(filename, 'r')
    key = ''
    value = ''
    for line in fi:
        line = line.strip()
        if line.startswith(">"): # header with lophiiformes
            # line = re.sub(" ","_", line)
            if key != '':
                fastadict[key] = value
            key = line[1:]
            value = '' #reset value for new header
            continue
        else:
            value += line.strip() # append to dictionary

##--taking the top hits from blast and making a list
def tophitsfromblast(filename, hits_list):
    fi = open(filename, 'r')
    for line in fi:
        cols = line.split("\t")
        hit = cols[1]
        # print(hit)
        hits_list.append(hit)

#taking top hits from balst, filtering the isoform, and making a list
def tophitsfromblast_filteringisoform(filename, hits_list):
    fi = open(filename, 'r')
    for line in fi:
        cols = line.split("\t")
        hit = cols[1]
        if "isoform" not in hit:
        # print(hit)
            hits_list.append(hit)

if __name__ == '__main__':
    print("Code is running don't worry!")
    fastadict={}
    filtered_dict = {}
    hits_list = []
    fastafile = sys.argv[1]
    blastinput = sys.argv[2]
    blastseqoutput = sys.argv[3]

    convertfastatodict_simple(fastafile)  
    tophitsfromblast_filteringisoform(blastinput, hits_list)
    hits_set = set(hits_list)
    hits_list = list(hits_set)
    for item in hits_list:
        for key, val in fastadict.items():
            if item == key:
                # print("Matching key is:" , key)
                filtered_dict[key] = val

    PrintDictToFastaFile(filtered_dict, blastseqoutput)

    ##-- howtorun
    ##-- python3 scriptname.py 
    ##--python3 blastmatchsequencesprotein.py dataset/vertebrates_protein.faa human_vertebratesdb_e5.txt human_vertebratesdb_e5_seq.faa