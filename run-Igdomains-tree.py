'''
##--This code will take in a folder with the Ig domains folder, and then align them and make into a tree. It will make slurm bash files and submit the job to the cluster
##--Go through the folder and check if there are fasta files, ending with _Igdomains in the folder. then use these tools on them
##-- Use famsa to align them. for this we need to load module famsa
##--Then use iqtree to make the tree.
Results can be stored in a igdomain-alignments folder. make the bashfiles that will be submitted into a folder called bashfiles-igdomains:
'''
import os
import subprocess
import sys

# Check if the path to the Ig domain folder is provided
if len(sys.argv) < 2:
    print("Usage: python script.py /path/to/Ig_domains")
    sys.exit(1)

# Directory containing Ig domain fasta files
ig_domain_folder = sys.argv[1]

# Output directories
alignment_folder = os.path.join(ig_domain_folder, 'igdomain-alignments')
bash_folder = os.path.join(ig_domain_folder, 'bashfiles-igdomains')

# Create output directories if they don't exist
os.makedirs(alignment_folder, exist_ok=True)
os.makedirs(bash_folder, exist_ok=True)

# SLURM template
slurm_template = """#!/bin/bash
#SBATCH --partition=Orion
#SBATCH --job-name={job_name}
#SBATCH --time=100:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=150GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=rmallik1@uncc.edu
#SBATCH --error=/scratch/rmallik1/SIRPS_newdata/log-EO-files/{job_name}.out

module load famsa
module load iqtree

famsa {input_file} {aligned_file}
iqtree2 -s {aligned_file} -m MFP -nt 8 -bb 5000 -redo
"""

# Iterate over Ig domain fasta files and create SLURM batch files
for file in os.listdir(ig_domain_folder):
    if file.endswith('_Igdomains_deduped.faa'):
        job_name = file.split('_Igdomains')[0]
        input_file = os.path.join(ig_domain_folder, file)
        aligned_file = os.path.join(alignment_folder, f'{job_name}_aligned.faa')
        bash_file = os.path.join(bash_folder, f'{job_name}.sh')

        # Fill in the SLURM template
        slurm_script = slurm_template.format(job_name=job_name,
                                             input_file=input_file,
                                             aligned_file=aligned_file)

        # Write the SLURM script to a file
        with open(bash_file, 'w') as f:
            f.write(slurm_script)

        # Submit the job to the cluster
        subprocess.run(['sbatch', bash_file])

##--usage
##--python SIRP-Seeker-Pypeline/run-Igdomains-tree.py /scratch/rmallik1/SIRPS_newdata/Ig-domains
