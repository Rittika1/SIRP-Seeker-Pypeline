"""

# Step 1: Provide an input directory containing confirmed SIRP sequences downloaded from NCBI. Currently includes human-sirp.fa, chicken-sirp.fa, and cattle-sirp.fa.

# Step 2: Execute BLAST using the specified database file name. The file is currently selected_vertebrate_proteins_noisoform.faa. Save results in a designated folder. The blast databse name is selected_vertebrates_protein.fa. Output file should be in the format human-sirp-vertebrates.blastout
blastp --query %s --db %s --threads 8 --max-target-seqs 0 --evalue 1e-10 --out %s
diamond blastp --query filename in inputDir --db inputdatabase --threads 8 --max-target-seqs 0 --evalue 1e-10 --out filename+blastdatabasename+blast.out
For example
diamond blastp --query filename in human.fa --db selected_vertebrate_proteins.faa --threads 8 --max-target-seqs 0 --evalue 1e-10 --out human-sirp-vertebrates.blastout

# Step 3: Utilize the BLAST results as input for a Python script to extract relevant sequences from the main vertebrates file. Take blast output file as input and run the python line. python3 scripts/blastmatchsequencesprotein.py '
python3 blastmatchsequencesprotein.py inputdatabase  human-sirp-vertebrates.blastout human-sirp-vertebrates_seq.faa

Step 3a: Add the sequences of the sirps to the big sequence files.
seqfilemaker = "cat filename in inputDir >> human-sirp-vertebrates_seq.faa"
# Step 4: Align the extracted sequences using FAMSA/MAFFT.
mafft --thread 8 --auto --inputorder --reorder  human-sirp-vertebrates_seq.faa > human-sirp-vertebrates_seq_mafft.faa

# Step 5: Apply IQTREE for additional analysis on the aligned sequences.
iqtree2 -s human-sirp-vertebrates_seq_mafft.faa -T 8

"""

# import sys

# inputDir = sys.argv[1]
# inputdatabase = sys.argv[2]

# proteinfileinput = sys.argv[1]

# blast_line_e10 =  'diamond blastp --query %s --db %s --threads 8 --max-target-seqs 0 --evalue 1e-10 --out %s'
# pythonseqline = 'python3 scripts/blastmatchsequencesprotein.py %s %s %s'
# seqfilemaker = "cat %s >> %s"
# mafft_line = "mafft --thread 8 --auto --inputorder --reorder  %s > %s"
# iqtree_line = "iqtree2 -s %s -T 8"
# bash_name = 'bashfiles/sirp-pipeline-%s.sh'


# # for root, dirs, file in os.walk(inputDir):
# #     sirpinput = filename
# #     blastoutput = filename+inputdatabase+"blast.out"
# #     blastline = " blastp -query" sirpinput "-db" inputdatabase -out blastoutput -max_target_seqs 1 -evalue 1e-10 -num_threads 12 -outfmt 6 "
# #     getsequencesline = "python3 blastmatchsequencesprotein.py dataset/vertebrates_protein.faa human_vertebratesdb_e5.txt human_vertebratesdb_e5_seq.faa"

# for root, dirs, files in os.walk("/scratch/rmallik1/PhD_EVILab/SIRPs", topdown=True):
#     # print(root)
#     for file in files:
#         filename = os.path.join(root,file)
#         if filename.endswith(".fa"):
#             # blastdatabasename = re.sub("_protein_filtered.faa", "filtereddb", proteinfileinput)
#             blastdatabasename = re.sub("_protein_filtered.faa", "", proteinfileinput) ## but take out only the vertebrates name
#             # blastoutfilelist = []
#             # for query in query_list:
#             identifier = re.sub(".fa", "", filename.split("/")[-1])
#             # print(root)
#             blastoutputfile5 = basefolder  + identifier+"_"+blastdatabasename.split("/")[-1]+"_e5.txt"
#             blastoutputfile10 = basefolder  + identifier+"_"+blastdatabasename.split("/")[-1]+"_e10.txt"
#             jobidentifier = re.sub("_e5.txt","",blastoutputfile5.split("/")[-1])
        
#             sequence_file10 = re.sub(".txt", "_noisoform_seq.faa", blastoutputfile10)
           
#             mafft_out10 = re.sub("_seq.faa", "_mafft.faa", sequence_file10)
#             # blastoutfilelist.append(blastoutputfile)
#             # print(blastoutputfile)    
#             # os.chdir('/scratch/rmallik1/PhD_EVILab/SIRPs/bashfiles/')    
#             with open(bash_name%jobidentifier, 'w') as bash_file:
#                 bash_file.writelines([bash_lines%(identifier, jobidentifier)] + [blast_line_e10%(filename , blastdatabasename, blastoutputfile10), '\n'] + [pythonseqline%(proteinfileinput, blastoutputfile10, sequence_file10), '\n'] + [seqfilemaker%(filename, sequence_file10), '\n'] + [mafft_line%(sequence_file10, mafft_out10), '\n']  + [iqtree_line%mafft_out10, '\n'])

import os
import sys
import re

def create_blast_command(query_file, database, output_file):
    return f'blastp -query {query_file} -db {database} -num_threads 8 -evalue 1e-10 -out {output_file}'

def create_python_sequence_command(input_database, blast_output, output_sequence):
    return f'python3 blastmatchsequencesprotein.py {input_database} {blast_output} {output_sequence}'

def create_seq_filemaker_command(input_file, output_sequence):
    return f'cat {input_file} >> {output_sequence}'

def create_mafft_command(input_sequence, output_aligned_sequence):
    return f'mafft --thread 8 --auto --inputorder --reorder {input_sequence} > {output_aligned_sequence}'

def create_iqtree_command(input_aligned_sequence):
    return f'iqtree2 -s {input_aligned_sequence} -T 8'

def create_bash_script(identifier, blast_database_name, input_file, base_folder):
    blast_output_file = os.path.join(base_folder, f"{identifier}_{blast_database_name}_e10.txt")
    sequence_file = os.path.join(base_folder, f"{identifier}_{blast_database_name}_seq.faa")
    aligned_sequence_file = os.path.join(base_folder, f"{identifier}_{blast_database_name}_mafft.faa")
    
    with open(os.path.join(base_folder+"/bashfiles", f"sirp-pipeline-{identifier}.sh"), 'w') as bash_file:
        bash_file.write(f"# Step 2: Execute BLAST\n")
        bash_file.write(create_blast_command(input_file, sys.argv[1], blast_output_file) + '\n\n')

        bash_file.write(f"# Step 3: Utilize BLAST results\n")
        bash_file.write(create_python_sequence_command(sys.argv[1], blast_output_file, sequence_file) + '\n')
        bash_file.write(f"# Step 3a: Add sequences to big sequence files\n")
        bash_file.write(create_seq_filemaker_command(input_file, sequence_file) + '\n\n')

        bash_file.write(f"# Step 4: Align extracted sequences using FAMSA/MAFFT\n")
        bash_file.write(create_mafft_command(sequence_file, aligned_sequence_file) + '\n\n')

        bash_file.write(f"# Step 5: Apply IQTREE for additional analysis\n")
        bash_file.write(create_iqtree_command(aligned_sequence_file) + '\n')

# Step 1: Provide an input directory containing confirmed SIRP sequences downloaded from NCBI.
# Currently includes human-sirp.fa, chicken-sirp.fa, and cattle-sirp.fa.

# Base folder for results
base_folder = "/home/rittika/Rittika-work/SIRPs_newdata"

for root, dirs, files in os.walk(sys.argv[2], topdown=True):
    for file in files:
        filename = os.path.join(root, file)
        if filename.endswith(".fa"):
            print("Filename: ",filename)
            blast_database_name = re.sub("_proteins_noisoform.faa", "", sys.argv[1])  # Extract the vertebrates name
            # print(blast_database_name)
            identifier = re.sub(".fa", "", filename.split("/")[-1])
            create_bash_script(identifier, blast_database_name, filename, base_folder)
