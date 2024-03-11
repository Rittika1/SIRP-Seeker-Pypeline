'''
This code takes a uniqueseq.phy file and then merges the Ig domains together, according to species. 
'''

def read_and_process_sequences(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Skip the first line

    sequences = {}
    for line in lines:
        parts = line.split()
        key = parts[0]
        gene_name = '_'.join(key.split('_')[:-1])  # Remove the last part after the last underscore
        sequence = parts[1].replace('-', '')  # Remove dashes from the sequence

        if gene_name in sequences:
            sequences[gene_name] += sequence  # Concatenate sequences for the same gene
        else:
            sequences[gene_name] = sequence

    return sequences

def write_fasta_output(gene_sequences, output_path):
    with open(output_path, 'w') as file:
        for gene_name, sequence in gene_sequences.items():
            file.write(f'>{gene_name}\n')
            for i in range(0, len(sequence), 80):
                file.write(f'{sequence[i:i+80]}\n')


def main():
    input_path = "Ig-domains/human-sirpa_hitdata_aligned_trimmed.faa.uniqueseq.phy"
    output_path = "Ig-domains/human-sirpa_hitdata_aligned_trimmed_merged.faa"

    sequences = read_and_process_sequences(input_path)
    write_fasta_output(sequences, output_path)

    print(f"Processed sequences have been written to {output_path}")

if __name__ == "__main__":
    main()
