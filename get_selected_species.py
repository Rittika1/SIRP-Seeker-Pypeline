import sys

def extract_species_name(header):
    # Extract species name from the first two words separated by "_"
    return '_'.join(header.split('_')[:2])

def filter_sequences(fasta_file, species_list_file, output_file):
    # Read the species names from the species list file
    with open(species_list_file, 'r') as species_file:
        species_list = [line.strip() for line in species_file]

    # Open the input fasta file and the output file
    with open(fasta_file, 'r') as input_file, open(output_file, 'w') as output_file:
        current_sequence = None
        current_species = None

        # Iterate through each line in the fasta file
        for line in input_file:
            if line.startswith('>'):
                # Extract species name from the sequence header
                current_species = extract_species_name(line[1:])
                current_sequence = line
            else:
                # If the current species is in the species list and "isoform" is not in the header, write the sequence to the output file
                if current_species in species_list and "isoform" not in current_sequence.lower():
                    output_file.write(current_sequence)
                    output_file.write(line)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python script.py <fasta_file> <species_list_file> <output_file>")
        sys.exit(1)

    # Get file paths from command-line arguments
    fasta_file_path = sys.argv[1]
    species_list_file_path = sys.argv[2]
    output_file_path = sys.argv[3]

    # Call the function with provided file paths
    filter_sequences(fasta_file_path, species_list_file_path, output_file_path)
    print("End of code")



##-----------HOW TO RUN----------------##
## python script.py path/to/your/fasta/file.fasta path/to/your/species/list/file.txt path/to/your/output/file.fasta
## python3 get_selected_species.py ../vertebrate_proteins_cleaned.faa species_list.txt selected_vertebrate_proteins_noisoform.faa
