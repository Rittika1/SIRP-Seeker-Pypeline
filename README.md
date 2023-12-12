# SIRP-Seeker-Pypeline
Detect Signal Regulatory Proteins (SIRPs) in diverse genomes using this Python and Bash pipeline. Genome-agnostic, modular, and documented for easy integration.

#SIRP Detection Workflow
This document outlines the step-by-step workflow for downloading vertebrate protein datasets, filtering selected species, and applying the SIRP detection pipeline. The pipeline involves using command-line tools and custom Python scripts.

##Downloading Vertebrate Protein Datasets
To download annotated vertebrate protein datasets, use the following command-line tool. For detailed information, visit NCBI Datasets Command-Line Documentation.

./datasets download genome taxon vertebrates --annotated --include protein --filename vertebrates_proteins.zip
