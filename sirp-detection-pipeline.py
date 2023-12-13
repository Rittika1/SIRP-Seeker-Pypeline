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

import os
import sys
import re

def create_blast_command(query_file, database, output_file):
    return f'echo "Running Step 2: Execute BLAST" && blastp -query {query_file} -db {database} -num_threads 8 -outfmt 6 -evalue 1e-10 -out {output_file}'

def create_python_sequence_command(input_database, blast_output, output_sequence):
    return f'echo "Running Step 3: Utilize BLAST results to get sequences" && python3 SIRP-Seeker-Pypeline/blastmatchsequencesprotein.py {input_database} {blast_output} {output_sequence}'

def create_seq_filemaker_command(input_file, output_sequence):
    return f'echo "Running Step 3a: Add confirmed SIRP sequences back to big sequence files" && cat {input_file} >> {output_sequence}'

def create_mafft_command(input_sequence, output_aligned_sequence):
    return f'echo "Running Step 4: Align extracted sequences using FAMSA/MAFFT" && mafft --thread 8 --auto --inputorder --reorder {input_sequence} > {output_aligned_sequence}'

def create_iqtree_command(input_aligned_sequence):
    return f'echo "Running Step 5: Apply IQTREE for additional analysis" && iqtree2 -s {input_aligned_sequence} -T 8'

def create_results_folder(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def create_bash_script(identifier, blast_database_name, input_file, base_folder):
    blast_folder = os.path.join(base_folder, "blast_results")
    sequence_folder = os.path.join(base_folder, "sequence_results")
    alignment_folder = os.path.join(base_folder, "alignment_results")
    bashfiles_folder = os.path.join(base_folder, "bashfiles")
    
    create_results_folder(blast_folder)
    create_results_folder(sequence_folder)
    create_results_folder(alignment_folder)
    create_results_folder(bashfiles_folder)

    blast_output_file = os.path.join(blast_folder, f"{identifier}_{blast_database_name}_e10.txt")
    sequence_file = os.path.join(sequence_folder, f"{identifier}_{blast_database_name}_seq.faa")
    aligned_sequence_file = os.path.join(alignment_folder, f"{identifier}_{blast_database_name}_mafft.faa")
    bash_file_path = os.path.join(bashfiles_folder, f"sirp-pipeline-{identifier}.sh")
    
    with open(bash_file_path, 'w') as bash_file:
        bash_file.write(f'# Step 2: Execute BLAST\n')
        bash_file.write(create_blast_command(input_file, sys.argv[1], blast_output_file) + '\n\n')

        bash_file.write(f'# Step 3: Utilize BLAST results to get sequences\n')
        bash_file.write(create_python_sequence_command(sys.argv[1], blast_output_file, sequence_file) + '\n')
        
        bash_file.write(f'# Step 3a: Add confirmed SIRP sequences back to big sequence files\n')
        bash_file.write(create_seq_filemaker_command(input_file, sequence_file) + '\n\n')

        bash_file.write(f'# Step 4: Align extracted sequences using FAMSA/MAFFT\n')
        bash_file.write(create_mafft_command(sequence_file, aligned_sequence_file) + '\n\n')

        bash_file.write(f'# Step 5: Apply IQTREE for additional analysis\n')
        bash_file.write(create_iqtree_command(aligned_sequence_file) + '\n')

        bash_file.write(f'\n# ------------------End of piepline. Go look at the trees now. Good luck! ----------------------\n')
        # bash_file.write(f'bash {bash_file_path}\n')

# Step 1: Provide an input directory containing confirmed SIRP sequences downloaded from NCBI.
# Currently includes human-sirp.fa, chicken-sirp.fa, and cattle-sirp.fa.

# sys.argv[1] is the name of the blast database
input_protein_database = sys.argv[1]
blast_database_name = re.sub(".faa", "", input_protein_database)

# sys.argv[2] is the input directory containing confirmed SIRP sequences
input_directory = sys.argv[2]

# sys.argv[3] is the base folder for results
base_folder = sys.argv[3]

for root, dirs, files in os.walk(input_directory, topdown=True):
    for file in files:
        filename = os.path.join(root, file)
        if filename.endswith(".fa"):
            identifier = re.sub(".fa", "", filename.split("/")[-1])
            create_bash_script(identifier, blast_database_name, filename, base_folder)
            # print("Running bash script for ", identifier)


##--------------HOW to run this code------------------##
#python script.py selected_vertebrates_protein.fa input_directory /path/to/basefolder
#python SIRP-Seeker-Pypeline/sirp-detection-pipeline.py selected_vertebrates_protein_noisoform.fa SIRP-seqs .