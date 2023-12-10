##----------Downloading data--------------------------------##
# Link to downloading the datasets command line tool
# https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/
# https://www.ncbi.nlm.nih.gov/datasets/docs/v2/reference-docs/command-line/datasets/download/genome/datasets_download_genome_taxon/

./datasets download genome taxon vertebrates --annotated --include protein --filename vertebrates_proteins.zip
####--- Tags explained
####--- --annotated to get only proteins, same reason for --include
##-- This downlaoded 1237 protein files. Dated Dec 2023

unzip vertebrates_proteins.zip
##-- This unzips the folder into a folder named ncbi_dataset, subfolder is data
##-- Inside data are 1237 subfolders of each species, with a file protein.faa inside each of them. We need to combine all the protein files into one mega protein file

cat ncbi_dataset/data/*/protein.faa >> vertebrate_proteins.faa
##