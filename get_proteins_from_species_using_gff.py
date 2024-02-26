'''
This code is used to extract proteins from a specific species using the gff file. The gff file has lines with columns of information about the gene locations, and the last column is delimited by ;. 

Function 1: get_chromosome_number_from_gff
Step1: Read the gff file and extract the lines with the chromosome number, it will in the pattern of "chromosome=10". this line will be in the Format:
        NC_041317.1	RefSeq	region	1	99678440	.	+	.	ID=NC_041317.1:1..99678440;Dbxref=taxon:64176;Name=6;chromosome=6;dev-stage=adult;ecotype=yellow;gbkey=Src;genome=chromosome;mol_type=genomic DNA;sex=male;tissue-type=muscle
Step2: In the line with the chromosome number, get the first column, and extract the lines having the same first column. This column is the chromosome region ID. The lines will be kept into a new file.
Note: The new file will be used to extract the proteins from the fasta file. The fasta file has the protein sequences of the genes. The fasta file has the following format:
        >NP_697020.2 beta-defensin 125 preproprotein [Homo sapiens]

Function 2: get_proteinID_startstop
    Get a list of the protein sequences and the start and stop of the genes

Step3: In the new file, the lines will be in this format:
    NC_000020.11	RefSeq	region	1	64444167	.	+	.	ID=NC_000020.11:1..64444167;Dbxref=taxon:9606;Name=20;chromosome=20;gbkey=Src;genome=chromosome;mol_type=genomic DNA
NC_000020.11	BestRefSeq	gene	87672	97094	.	+	.	ID=gene-DEFB125;Dbxref=GeneID:245938,HGNC:HGNC:18105;Name=DEFB125;description=defensin beta 125;gbkey=Gene;gene=DEFB125;gene_biotype=protein_coding;gene_synonym=DEFB-25
NC_000020.11	BestRefSeq	mRNA	87672	97094	.	+	.	ID=rna-NM_153325.4;Parent=gene-DEFB125;Dbxref=Ensembl:ENST00000382410.3,GeneID:245938,GenBank:NM_153325.4,HGNC:HGNC:18105;Name=NM_153325.4;gbkey=mRNA;gene=DEFB125;product=defensin beta 125;tag=MANE Select;transcript_id=NM_153325.4
NC_000020.11	BestRefSeq	exon	87672	87767	.	+	.	ID=exon-NM_153325.4-1;Parent=rna-NM_153325.4;Dbxref=Ensembl:ENST00000382410.3,GeneID:245938,GenBank:NM_153325.4,HGNC:HGNC:18105;gbkey=mRNA;gene=DEFB125;product=defensin beta 125;tag=MANE Select;transcript_id=NM_153325.4
NC_000020.11	BestRefSeq	exon	96005	97094	.	+	.	ID=exon-NM_153325.4-2;Parent=rna-NM_153325.4;Dbxref=Ensembl:ENST00000382410.3,GeneID:245938,GenBank:NM_153325.4,HGNC:HGNC:18105;gbkey=mRNA;gene=DEFB125;product=defensin beta 125;tag=MANE Select;transcript_id=NM_153325.4
NC_000020.11	BestRefSeq	CDS	87710	87767	.	+	0	ID=cds-NP_697020.2;Parent=rna-NM_153325.4;Dbxref=CCDS:CCDS12989.2,Ensembl:ENSP00000371847.2,GeneID:245938,GenBank:NP_697020.2,HGNC:HGNC:18105;Name=NP_697020.2;gbkey=CDS;gene=DEFB125;product=beta-defensin 125 preproprotein;protein_id=NP_697020.2;tag=MANE Select
NC_000020.11	BestRefSeq	CDS	96005	96417	.	+	2	ID=cds-NP_697020.2;Parent=rna-NM_153325.4;Dbxref=CCDS:CCDS12989.2,Ensembl:ENSP00000371847.2,GeneID:245938,GenBank:NP_697020.2,HGNC:HGNC:18105;Name=NP_697020.2;gbkey=CDS;gene=DEFB125;product=beta-defensin 125 preproprotein;protein_id=NP_697020.2;tag=MANE Select

Split the new line by tabs/spaced. In the line where the 3rd column is "gene", the 9th column will have the gene name, in the format: ID=gene-DEFB125.
So geneID is DEFB125. Store the values of the 4th and 5th column as the start and stop of the gene. This can be made into a tuple or list.

Search the next lines with the 3rd column as CDS, and the same geneID, and the phrase "protein_id". 
Protein_id will be in the format: protein_id=NP_697020.2 
The information of the protein_id and the start and stop of the gene will be stored in a dictionary. where the key is the protein_id and the value is a list of the start and stop of the gene.
This can be written into a file with the sampleID, protein_id, start and stop of the gene. sampleID to be provided by user

Function 3: get_protein_seq_from_fasta
    Get the protein sequence from the fasta file
    Store the protein_ids in a list, from the dictionary in the previous function
    Read the fasta file and extract the protein sequences of the protein_ids, by checking which sequences have the protein_ids in the sequence header file.

So the total inputs will be the gff file, the fasta file, and the species name. The species name will be used to extract the proteins from the gff file. The gff file will be used to extract the protein_ids and the start and stop of the genes. The fasta file will be used to extract the protein sequences of the protein_ids.
'''
import sys
import os
from Bio import SeqIO
import re

def get_chromosome_number_from_gff(gff_file, chromosome_number):
    output_file = f'chromosome_{chromosome_number}_specific.gff'
    with open(gff_file, 'r') as gff, open(output_file, 'w') as out:
        for line in gff:
            if 'chromosome=' + str(chromosome_number) in line:
                chrom_id = line.split('\t')[0]
                break
        gff.seek(0)  # Reset to start of file
        for line in gff:
            if line.startswith(chrom_id) and not line.startswith('#'):
                out.write(line)
    return output_file

def get_proteinID_startstop(input_file, sampleID):
    protein_info = {}
    gene_positions = {}
    output_file = sampleID + "_gene_positions.txt"
    with open(input_file, 'r') as infile:
        for line in infile:
            columns = line.strip().split('\t')
            if columns[2] == 'gene':
                gene_id_match = re.search(r'ID=gene-([^;]+)', columns[8])
                if gene_id_match:
                    gene_id = gene_id_match.group(1)
                    start_stop = (columns[3], columns[4])
                    gene_positions[gene_id] = start_stop
            elif columns[2] == 'CDS' and 'protein_id' in columns[8]:
                protein_id_match = re.search(r'protein_id=([^;]+)', columns[8])
                if protein_id_match:
                    protein_id = protein_id_match.group(1)
                    for gene, positions in gene_positions.items():
                        if gene in columns[8]:
                            protein_info[protein_id] = positions

    # Write unique entries to file
    with open(output_file, 'w') as outfile:
        for protein_id, positions in protein_info.items():
            outfile.write(f'{sampleID}\t{protein_id}\t{positions[0]}\t{positions[1]}\n')

    return protein_info

def get_protein_seq_from_fasta(fasta_file, protein_ids, sampleID):
    protein_sequences = {}
    output_fasta_file = sampleID + "_protein_seq.fasta"
    with open(fasta_file, "r") as fasta, open(output_fasta_file, "w") as outfile:
        for record in SeqIO.parse(fasta, "fasta"):
            for protein_id in protein_ids:
                if protein_id in record.description:
                    protein_sequences[protein_id] = str(record.seq)
                    outfile.write(f'>{record.description}\n{str(record.seq)}\n')
    return protein_sequences

def main():
    # Get the gff file, fasta file, chromosome number, and sample ID from the user
    gff_file = sys.argv[1]
    fasta_file = sys.argv[2]
    chromosome_number = sys.argv[3]
    sampleID = sys.argv[4]

    # Extract chromosome-specific information from the gff file
    chromosome_number_file = get_chromosome_number_from_gff(gff_file, chromosome_number)

    # Extract the protein ID, start, and stop of the genes, and generate a positions file
    gene_dict = get_proteinID_startstop(chromosome_number_file, sampleID)

    # Extract the protein sequences from the fasta file and retain full headers
    get_protein_seq_from_fasta(fasta_file, gene_dict.keys(), sampleID)

    # Clean up intermediate file
    os.remove(chromosome_number_file)

if __name__ == "__main__":
    main()



#Run the code
#python extract_proteins.py path/to/your/file.gff path/to/your/sequences.fasta 6 YourSampleID
#python3 get_proteins_from_species_using_gff.py lizard/lizard_genomic.gff lizard/lizard_protein.faa 6 pm-chr6
#python get_proteins_from_species_using_gff.py gff_file fasta_file chromosome_number sampleID