##--Downloading vertebrate protein datasets with the command line tool.
##--For details, visit: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/
##--Specific page: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/reference-docs/command-line/datasets/download/genome/datasets_download_genome_taxon/

./datasets download genome taxon vertebrates --annotated --include protein --filename vertebrates_proteins.zip

##--Tags Explanation:
##----annotated: Retrieves only annotated proteins.
##----include protein: Similar reason as above.

##--Downloaded 1237 protein files as of Dec 2023.

##--Unzipping the downloaded file into the 'ncbi_dataset' folder.
##--Inside 'ncbi_dataset', there's a 'data' subfolder containing 1237 species subfolders.
##--Each species subfolder has a 'protein.faa' file. We need to merge them into one mega protein file.

unzip vertebrates_proteins.zip

##--Concatenating all 'protein.faa' files into 'vertebrate_proteins.faa'.
cat ncbi_dataset/data/*/protein.faa >> vertebrate_proteins.faa

##--Next step: Filtering out selected species from 'vertebrate_proteins.faa'.
# Refer to 'species_list.txt'. This will be accomplished using a Python script.
## python get_selected_species.py path/to/your/fasta/file.fasta path/to/your/species/list/file.txt path/to/your/output/file.fasta

python3 get_selected_species.py ../vertebrate_proteins_cleaned.faa species_list.txt selected_vertebrate_proteins_noisoform.faa

##--Appending two additional protein files annotated using Braker to the existing fasta file.
##--No further modifications are necessary at this point. Below is the code snippet for reference.
## cat Lepisosteus_osseus_proteins.fa >> selected_vertebrate_proteins_noisoform.faa
## cat bichir_braker_proteins.fa >> selected_vertebrate_proteins_noisoform.faa

##After this step, we need to make a database from the proteins file. I am using NCBI BLAST as we have made our protein file much smaller now.
##--databasefasta=$1
##--makeblastdb -in $1 -dbtype prot
makeblastdb -in selected_vertebrate_proteins_noisoform.faa -dbtype prot

##-- Creating a separate folder named SIRP-seqs containing confirmed sequences for each species.

##-- The following section represents a repeating part of the entire pipeline.
##-- A separate script will be created for this section to be used as a standalone part.
python SIRP-Seeker-Pypeline/sirp-detection-pipeline.py database/selected_vertebrate_proteins_noisoform.faa SIRP-seqs .

##-----For Ian, since you will be running the ligands part of the pipeline, you will need to run the following code snippet.
##-----Make a separate folder named 'ligands' containing confirmed sequences for each species. I have made that folder for you. 
##-----The following code snippet will be used for running the ligands part of the pipeline.
python SIRP-Seeker-Pypeline/sirp-detection-pipeline.py database/selected_vertebrate_proteins_noisoform.faa ligands .

##--The python line will make the necessary bashfiles and store them in the bashfiles folder. For running the bashfiles, we will use the following code snippet. 
##-- This path of the bashfiles folder will need to be changed for the ligands part of the pipeline.

for file in bashfiles_SIRP-seqs/*.sh ; do
    echo "Running $file"
    bash "$file"
done