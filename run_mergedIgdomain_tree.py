import os
import subprocess

# Directory paths
input_dir = 'Ig-domains/trimmed-aliview'
output_dir = 'Ig-domains/bashfiles-igdomains'
python_script_path = '/scratch/rmallik1/SIRPS_newdata/SIRP-Seeker-Pypeline/merge-Igdomains.py'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop through files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.faa'):
        # Extract the base name without extension
        base_name = filename.rsplit('.', 1)[0]
        job_name = base_name.replace('-', '_')

        # Create the SLURM script content
        slurm_script = f"""#!/bin/bash
#SBATCH --partition=Orion
#SBATCH --job-name={job_name}
#SBATCH --time=100:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem=64GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=rmallik1@uncc.edu
#SBATCH --error=/scratch/rmallik1/SIRPS_newdata/log-EO-files/{job_name}.out

module load famsa
module load iqtree

cd /scratch/rmallik1/SIRPS_newdata/

python3 {python_script_path} {os.path.join(input_dir, filename)} {os.path.join(input_dir, base_name)}_merged.faa
famsa {os.path.join(input_dir, base_name)}_merged.faa {os.path.join(input_dir, base_name)}_merged_aligned.faa
iqtree2 -s {os.path.join(input_dir, base_name)}_merged_aligned.faa -m MFP -nt 16 -bb 5000
"""

        # Write the SLURM script to a file
        script_path = os.path.join(output_dir, f'{base_name}.slurm')
        with open(script_path, 'w') as script_file:
            script_file.write(slurm_script)

        # Submit the SLURM job
        subprocess.run(['sbatch', script_path])
