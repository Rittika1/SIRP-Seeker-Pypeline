import re
import os
import sys


'''
There are two files: 
one is a fasta file 'cattle-sirpa_seq.faa' in this format:
>Polypterus_bichir_Sc1mPbE_25916.HRSCAF=26416.g1520.t1
XFNVSQPQGRVEALERSNVTLVCVVSSESPLGPVRWYKGAGSERTHFYSAAPKGGDKSDPRVTWTMENPT
VNFSITIRDLRVSDTGEYYCEKYTKADNKSKPYASGPGVTLTVRGGRHSLTLSSLCVF*

Other file 'hitdata.txt' looks like this:
#Batch CD-search tool	NIH/NLM/NCBI
#Start time	2024-02-13T17:04:06	Run time	0:00:08:58
#status	success

Query	Hit type	PSSM-ID	From	To	E-Value	Bitscore	Accession	Short name	Incomplete	Superfamily
Q#2 - >Polypterus_bichir_Sc1mPbE_25916.HRSCAF=26416.g1520.t1	superfamily	448366	4	114	1.65378e-18	74.8992	cl11960	Ig superfamily	 - 	 - 
Q#3 - >Rousettus_aegyptiacus_KAF6422750.1_hypothetical_protein_HJG63_008564	specific	409516	35	144	2.83912e-73	215.882	cd16097	IgV_SIRP	 - 	cl11960
Q#4 - >Dromaius_novaehollandiae_XP_025962855.1_tyrosine-protein_phosphatase_non-receptor_type_substrate_1-like,_partial	superfamily	448366	48	150	3.43241e-27	100.708	cl11960	Ig superfamily	 - 	 - 
Q#5 - >Homo_sapiens_KAI4004538.1_signal_regulatory_protein_beta_2	superfamily	448366	161	264	8.16413e-31	112.649	cl11960	Ig superfamily	 - 	 - 
Q#5 - >Homo_sapiens_KAI4004538.1_signal_regulatory_protein_beta_2	superfamily	448366	40	150	5.78675e-22	89.1516	cl11960	Ig superfamily	 - 	 - 

in the second file, we want to parse it and create a temp file that ignores the lines starting with #, 
and then only keep the lines starting with Q. also only keep the lines with the string "superfamily" in them.
From this temp file, create a dictionary with the '>Polypterus_bichir_Sc1mPbE_25916.HRSCAF=26416.g1520.t1' part
which should be the 2nd or 3rd column, as the key. the values will be the pair 4,114. 
For the ones having more lines with same key, make a list of the values like 
>Homo_sapiens_KAI4004538.1_signal_regulatory_protein_beta_2	as key and value is	[[161,264],	[40,150]]

Using this dictionary, we will filter out fasta sequences from the first file. The values are the starting and ending positions of a substring.
In the fasta file, match the key with the fasta sequence header.
the sequences have to be cut off according to the values in the dictionary. 
So for the sequence :
>Polypterus_bichir_Sc1mPbE_25916.HRSCAF=26416.g1520.t1
XFNVSQPQGRVEALERSNVTLVCVVSSESPLGPVRWYKGAGSERTHFYSAAPKGGDKSDPRVTWTMENPT
VNFSITIRDLRVSDTGEYYCEKYTKADNKSKPYASGPGVTLTVRGGRHSLTLSSLCVF*

the other file says: 
>Polypterus_bichir_Sc1mPbE_25916.HRSCAF=26416.g1520.t1 [4,114] , so the new sequences will be cut off from position 4 and till 
position 114, and then pasted into a new file int his format:
>Polypterus_bichir_Sc1mPbE_25916.HRSCAF=26416.g1520.t1_Ig1
the number _Ig1 can increase if there are moer values.
like >Homo_sapiens_KAI4004538.1_signal_regulatory_protein_beta_2	will have _Ig1 and _Ig2 due to having 2 values.

'''
import sys
import os

def parse_hitdata(file_path):
    hit_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('Q') and 'superfamily' in line:
                parts = line.split('\t')
                key = parts[0].split('>')[1].strip()
                value = [int(parts[3]), int(parts[4])]
                
                if key in hit_dict:
                    hit_dict[key].append(value)
                else:
                    hit_dict[key] = [value]
    return hit_dict

def filter_fasta_sequences(fasta_file_path, hit_dict, output_file_path):
    with open(fasta_file_path, 'r') as fasta_file, open(output_file_path, 'w') as output_file:
        header = None
        sequence = ''
        for line in fasta_file:
            if line.startswith('>'):
                if header and sequence:
                    key = header[1:].strip()
                    if key in hit_dict:
                        for idx, (start, end) in enumerate(hit_dict[key], start=1):
                            new_header = f"{header.strip()}_Ig{idx}\n"
                            new_sequence = sequence[start - 1:end] + '\n'
                            output_file.write(new_header)
                            output_file.write(new_sequence)
                header = line
                sequence = ''
            else:
                sequence += line.strip()
        # Write the last sequence
        if header and sequence:
            key = header[1:].strip()
            if key in hit_dict:
                for idx, (start, end) in enumerate(hit_dict[key], start=1):
                    new_header = f"{header.strip()}_Ig{idx}\n"
                    new_sequence = sequence[start - 1:end] + '\n'
                    output_file.write(new_header)
                    output_file.write(new_sequence)


def remove_duplicate_sequences(fasta_file_path, output_file_path):
    sequences = {}
    with open(fasta_file_path, 'r') as fasta_file:
        header = None
        sequence = ''
        for line in fasta_file:
            if line.startswith('>'):
                if header and sequence:
                    if sequence not in sequences:
                        sequences[sequence] = header
                header = line.strip()
                sequence = ''
            else:
                sequence += line.strip()
        # Write the last sequence
        if header and sequence:
            if sequence not in sequences:
                sequences[sequence] = header

    with open(output_file_path, 'w') as output_file:
        for sequence, header in sequences.items():
            output_file.write(f"{header}\n{sequence}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <hitdata_file> <fasta_file>")
        sys.exit(1)

    hitdata_file = sys.argv[1]
    fasta_file = sys.argv[2]
    fasta_base = os.path.splitext(hitdata_file)[0]
    filtered_file = f"{fasta_base}_Igdomains.faa"
    deduped_file = f"{fasta_base}_Igdomains_deduped.faa"

    hit_dict = parse_hitdata(hitdata_file)
    filter_fasta_sequences(fasta_file, hit_dict, filtered_file)
    remove_duplicate_sequences(filtered_file, deduped_file)
    print(f"Filtered and deduplicated sequences have been written to {deduped_file}")

    ##Usage
    ##python get-Igdomains.py hitdata.txt cattle-sirpa_seq.faa
    ##python SIRP-Seeker-Pypeline/get-Igdomains.py Ig-domains/cattle-sirpa_hitdata.txt sequence_results/cattle-sirpa_seq.faa
    ##--python SIRP-Seeker-Pypeline/get-Igdomains.py Ig-domains/chicken-sirpa_hitdata.txt sequence_results/chicken-sirp_seq.faa
    ##--python SIRP-Seeker-Pypeline/get-Igdomains.py Ig-domains/human-sirpa_hitdata.txt sequence_results/human-sirp_seq.faa

