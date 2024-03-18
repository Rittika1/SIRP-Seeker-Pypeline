# SIRP-Seeker-Pypeline
Detect Signal Regulatory Proteins (SIRPs) in diverse genomes using this Python and Bash pipeline. Genome-agnostic, modular, and documented for easy integration.

## Clone this repo
You can clone this repo using 
`git clone git@github.com:Rittika1/SIRP-Seeker-Pypeline.git`

## Pre-requisites softwares for this
You will need to install blast, mafft and iqtree for this. I am giving the links to download and install them. I can add code to run this on the cluster if you need to

[BLAST](https://www.metagenomics.wiki/tools/blast/install)

[MAFFT](https://mafft.cbrc.jp/alignment/software/)

[IQTREE](http://www.iqtree.org/doc/Download)

## Pre-requisites python packages for this
You will need to install the following python packages for this
- pandas
- numpy
- biopython
- tqdm
- subprocess
- os
- sys
- re
- argparse

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

Making sure you have downlaoded only one assembly of each species
------------------------------------------------------------------

Use the script `SIRP-Seeker-Pypeline/remove-multiple-assemblies-persp.py` to make a not of how many assemblies are there per species. This code concatenates the individual protein files into one mega protein file. This protein file is called vertebrates_proteins.faa

Unzipping and Concatenating Protein Files
-----------------------------------------

Unzip the downloaded file into the 'ncbi_dataset' folder. Inside 'ncbi_dataset', there's a 'data' subfolder containing 1237 species subfolders. Each species subfolder has a 'protein.faa' file. Concatenate all 'protein.faa' files into 'vertebrate_proteins.faa'.

`unzip vertebrates_proteins.zip
cat ncbi_dataset/data/*/protein.faa >> vertebrate_proteins.faa`

Filtering Selected Species
--------------------------
Arrange the speices names properly in the fasta file using this code:
`python3 SIRP-Seeker-Pypeline/filteringproteinfiles.py vertebrate_proteins.faa vertebrate_proteins_cleaned.faa`

Filter out selected species from 'vertebrate_proteins.faa' using the Python script 'get_selected_species.py'. Provide the path to your fasta file, species list file, and the output file.

` python3 SIRP-Seeker-Pypeline/get_selected_species.py  vertebrate_proteins_cleaned.faa SIRP-Seeker-Pypeline/species_list.txt database/selected_vertebrate_proteins_noisoform.faa`

Appending Additional Protein Files
----------------------------------

Append two additional protein files annotated using Braker to the existing fasta file. Do not include the osseus as it is very fragmented

`cat Lepisosteus_osseus_proteins.fa >> database/selected_vertebrate_proteins_noisoform.faa 
cat bichir_braker_proteins.fa >> database/selected_vertebrate_proteins_noisoform.faa`

Creating BLAST Database
-----------------------
Make a folder named database and transfer the protein file there

After modifying the protein file, create a database using NCBI BLAST.

`makeblastdb -in selected_vertebrate_proteins_noisoform.faa -dbtype prot`

SIRP Detection Pipeline
-----------------------

Create a separate folder named 'SIRP-seqs' containing confirmed sequences for each species. Such a folder can also be made with ligands, and add the CD47 sequences to it.

The following section represents a repeating part of the entire pipeline. A separate script will be created for this section to be used as a standalone part. The code above have to be run only once and it is done already


`python SIRP-Seeker-Pypeline/sirp-detection-pipeline.py database/selected_vertebrate_proteins_noisoform.faa SIRP-seqs .`

The Python script will generate necessary bashfiles and store them in the 'bashfiles' folder. To run the bashfiles, use the following code snippet.


`for file in bashfiles/*.sh ; do
    echo "Running $file"
    bash "$file"
done`

This completes the SIRP detection workflow, including downloading datasets, filtering species, and running the pipeline.

# Ig domain detection
After getting the possible SIRPS detected and aligned, we need to find the Immunoglobulin domains. To do this, we have to use the NCBI CDD database available at `https://www.ncbi.nlm.nih.gov/Structure/bwrpsb/bwrpsb.cgi`

Here, we upload the sequence file that are obtained after the first round of the pipeline. So the files under the sequence_results will be used. 
The result will come as a text file as cattle-sirpa-hitdata.txt.
To get the sequences of the Ig domains, we run the code `SIRP-Seeker-Pypeline/get-Igdomains.py`. 

I ran these three lines:
`python SIRP-Seeker-Pypeline/get-Igdomains.py Ig-domains/cattle-sirpa_hitdata.txt sequence_results/cattle-sirpa_seq.faa
python SIRP-Seeker-Pypeline/get-Igdomains.py Ig-domains/chicken-sirpa_hitdata.txt sequence_results/chicken-sirp_seq.faa
python SIRP-Seeker-Pypeline/get-Igdomains.py Ig-domains/human-sirpa_hitdata.txt sequence_results/human-sirp_seq.faa`

After this, run the `SIRP-Seeker-Pypeline/run-Igdomains-tree.py` code to get the alignment and the tree running on the cluster. For that I ran the code:

`python SIRP-Seeker-Pypeline/run-Igdomains-tree.py /scratch/rmallik1/SIRPS_newdata/Ig-domains`

this will run the famsa and IQTREE2 and save the results into the folder `Ig-domains/igdomain-alignments/`

# Trimming Ig domains
The files named like  'human-sirpa_hitdata_aligned.faa' were opened using ALiview. any sequences that were long and on either side of the domains were trimmed and named as 'Ig-domains/trimmed-aliview/cattle-sirpa_hitdata_aligned_trimmed.faa'. 

# Merging Ig domains to get full genes
The trimmed Ig domains were then merged back using the code `SIRP-Seeker-Pypeline/merge-Igdomains.py` to get back the full genes per species. These files were named as _trimmed.faa.

After these run the code `SIRP-Seeker-Pypeline/run_mergedIgdomain_tree.py` to merge these genes, align these and get the tree that it makes. This is ahrd coded I ran out of time to automate this


# Phylogenetic signal calculation
run the code `SIRP-Seeker-Pypeline/phylosignal-igdomains.R`. This takes in the input of the hitdata file from the NCBI CDD database. Prints out K and Lambda

# Paralog count and plotting
run the code like this 
 
`python3 SIRP-Seeker-Pypeline/countparalogs.py Ig-domains/trimmed-aliview/human-sirpa_hitdata_aligned_trimmed_merged.faa > paralogs/human-sirp-paralogs.txt`
`cut -f 1 human-sirp-paralogs.txt > human-sirp-paralog-species.txt`
After this, upload the species file to timetree.org to get a newick file. Save all these three files in the paralogs folder.
Plot using the R code `SIRP-Seeker-Pypeline/plot-paralogs.R`

# Igdomain count and plotting