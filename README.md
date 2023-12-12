# SIRP-Seeker-Pypeline
Detect Signal Regulatory Proteins (SIRPs) in diverse genomes using this Python and Bash pipeline. Genome-agnostic, modular, and documented for easy integration.

## Clone this repo
You can clone this repo using 
`git clone git@github.com:Rittika1/SIRP-Seeker-Pypeline.git`

# SIRP Detection Workflow
This document outlines the step-by-step workflow for downloading vertebrate protein datasets, filtering selected species, and applying the SIRP detection pipeline. The pipeline involves using command-line tools and custom Python scripts.

## Downloading Vertebrate Protein Datasets
To download annotated vertebrate protein datasets, use the following command-line tool. For detailed information, visit NCBI Datasets Command-Line Documentation.

```bash
./datasets download genome taxon vertebrates --annotated --include protein --filename vertebrates_proteins.zip
```
Tags Explanation:

-   `annotated`: Retrieves only annotated proteins.
-   `include protein`: Similar reason as above.

As of December 2023, 1237 protein files have been downloaded.

Unzipping and Concatenating Protein Files
-----------------------------------------

Unzip the downloaded file into the 'ncbi_dataset' folder. Inside 'ncbi_dataset', there's a 'data' subfolder containing 1237 species subfolders. Each species subfolder has a 'protein.faa' file. Concatenate all 'protein.faa' files into 'vertebrate_proteins.faa'.

`unzip vertebrates_proteins.zip
cat ncbi_dataset/data/*/protein.faa >> vertebrate_proteins.faa`

Filtering Selected Species
--------------------------

Filter out selected species from 'vertebrate_proteins.faa' using the Python script 'get_selected_species.py'. Provide the path to your fasta file, species list file, and the output file.

`python3 get_selected_species.py vertebrate_proteins.faa species_list.txt selected_vertebrate_proteins_noisoform.faa`

Appending Additional Protein Files
----------------------------------

Append two additional protein files annotated using Braker to the existing fasta file.

`cat Lepisosteus_osseus_proteins.fa >> selected_vertebrate_proteins_noisoform.faa
cat bichir_braker_proteins.fa >> selected_vertebrate_proteins_noisoform.faa`

Creating BLAST Database
-----------------------

After modifying the protein file, create a database using NCBI BLAST.

`makeblastdb -in selected_vertebrate_proteins_noisoform.faa -dbtype prot`

SIRP Detection Pipeline
-----------------------

Create a separate folder named 'SIRP-seqs' containing confirmed sequences for each species. Such a folder can also be made with ligands, and add the CD47 sequences to it.

The following section represents a repeating part of the entire pipeline. A separate script will be created for this section to be used as a standalone part. The code above have to be run only once and it is done already


`python SIRP-Seeker-Pypeline/sirp-detection-pipeline.py selected_vertebrate_proteins_noisoform.faa SIRP-seqs .`

The Python script will generate necessary bashfiles and store them in the 'bashfiles' folder. To run the bashfiles, use the following code snippet.


`for file in bashfiles/*.sh ; do
    echo "Running $file"
    bash "$file"
done`

This completes the SIRP detection workflow, including downloading datasets, filtering species, and running the pipeline.
