'''
This code takes a alignment fasta file and then merges the Ig domains together, according to species. 
'''
import sys

def read_and_process_input(file_path):
    gene_sequences = {}
    current_gene_name = ""
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                current_gene_name = line[1:].rsplit('_', 1)[0]
            else:
                sequence = line.replace('-', '')
                if current_gene_name in gene_sequences:
                    gene_sequences[current_gene_name] += sequence
                else:
                    gene_sequences[current_gene_name] = sequence
    return gene_sequences

def write_fasta_output(gene_sequences, output_path):
    with open(output_path, 'w') as file:
        for gene_name, sequence in gene_sequences.items():
            file.write(f'>{gene_name}\n')
            for i in range(0, len(sequence), 80):
                file.write(f'{sequence[i:i+80]}\n')

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py input.fasta output.fasta")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    gene_sequences = read_and_process_input(input_path)
    write_fasta_output(gene_sequences, output_path)

if __name__ == '__main__':
    main()

