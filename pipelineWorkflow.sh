# Downloading vertebrate protein datasets with the command line tool.
# For details, visit: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/
# Specific page: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/reference-docs/command-line/datasets/download/genome/datasets_download_genome_taxon/

./datasets download genome taxon vertebrates --annotated --include protein --filename vertebrates_proteins.zip

# Tags Explanation:
# --annotated: Retrieves only annotated proteins.
# --include protein: Similar reason as above.

# Downloaded 1237 protein files as of Dec 2023.

# Unzipping the downloaded file into the 'ncbi_dataset' folder.
# Inside 'ncbi_dataset', there's a 'data' subfolder containing 1237 species subfolders.
# Each species subfolder has a 'protein.faa' file. We need to merge them into one mega protein file.

unzip vertebrates_proteins.zip

# Concatenating all 'protein.faa' files into 'vertebrate_proteins.faa'.
cat ncbi_dataset/data/*/protein.faa >> vertebrate_proteins.faa

# Next step: Filtering out selected species from 'vertebrate_proteins.faa'.
# Refer to 'species_list.txt'. This will be accomplished using a Python script.
## python get_selected_species.py path/to/your/fasta/file.fasta path/to/your/species/list/file.txt path/to/your/output/file.fasta

python3 get_selected_species.py ../vertebrate_proteins_cleaned.faa species_list.txt selected_vertebrate_proteins_noisoform.faa

## After this I added two more proteins file to this fasta which were annotated using Braker. There is no need to do this further. Here is the code to do it just in case.
## cat Lepisosteus_osseus_proteins.fa >> selected_vertebrate_proteins_noisoform.faa
## cat bichir_braker_proteins.fa >> selected_vertebrate_proteins_noisoform.faa


##After this step, we need to make a database from the proteins file. I am using NCBI BLAST as we have made our protein file much smaller now.

