import sys

def read_fasta(fasta_file):
    """Reads a FASTA file and returns a dictionary of sequences."""
    sequences = {}
    with open(fasta_file, 'r') as file:
        sequence_id = ''
        sequence = ''
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                # print("line in fasta: ", line)
                if sequence_id:
                    sequences[sequence_id] = sequence
                sequence_id = line[1:]
                # print(sequence_id)
                sequence = ''
            else:
                sequence += line
        if sequence_id:
            sequences[sequence_id] = sequence
    return sequences

def read_patterns(patterns_file):
    """Reads a file containing patterns and returns them as a set."""
    with open(patterns_file, 'r') as file:
        return set(line.strip() for line in file)

def filter_sequences(sequences, patterns_to_remove):
    """Removes sequences whose header contains any of the specified patterns."""
    return {header: seq for header, seq in sequences.items() if not any(pattern in header for pattern in patterns_to_remove)}

def write_fasta(sequences, output_file):
    """Writes sequences to a FASTA file."""
    with open(output_file, 'w') as file:
        for header, sequence in sequences.items():
            # print(f'Writing header: {header}')  # Add this line to check the headers
            file.write(f'>{header}\n')
            file.write(f'{sequence}\n')


def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py input.fasta patterns_to_remove.txt output.fasta")
        sys.exit(1)

    fasta_file = sys.argv[1]
    patterns_file = sys.argv[2]
    output_file = sys.argv[3]

    sequences = read_fasta(fasta_file)
    patterns_to_remove = read_patterns(patterns_file)
    filtered_sequences = filter_sequences(sequences, patterns_to_remove)
    write_fasta(filtered_sequences, output_file)

    print(f'Filtered sequences have been written to {output_file}')

if __name__ == '__main__':
    main()
