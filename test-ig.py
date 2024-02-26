def parse_hitdata(file_path):
    hit_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('Q') and 'superfamily' in line:
                parts = line.split('\t')
                print("Parts: ", parts)
                key = parts[0].split('>')[1].strip()
                value = [int(parts[3]), int(parts[4])]
                
                if key in hit_dict:
                    hit_dict[key].append(value)
                else:
                    hit_dict[key] = [value]
    return hit_dict

def filter_fasta_sequences(fasta_file_path, hit_dict, output_file_path):
    with open(fasta_file_path, 'r') as fasta_file, open(output_file_path, 'w') as output_file:
        header = None
        sequence = ''
        for line in fasta_file:
            if line.startswith('>'):
                if header and sequence:
                    key = header[1:].strip()
                    if key in hit_dict:
                        for idx, (start, end) in enumerate(hit_dict[key], start=1):
                            new_header = f"{header.strip()}_Ig{idx}\n"
                            new_sequence = sequence[start - 1:end] + '\n'
                            output_file.write(new_header)
                            output_file.write(new_sequence)
                header = line
                sequence = ''
            else:
                sequence += line.strip()
        # Write the last sequence
        if header and sequence:
            key = header[1:].strip()
            if key in hit_dict:
                for idx, (start, end) in enumerate(hit_dict[key], start=1):
                    new_header = f"{header.strip()}_Ig{idx}\n"
                    new_sequence = sequence[start - 1:end] + '\n'
                    output_file.write(new_header)
                    output_file.write(new_sequence)
# Usage
hit_dict = parse_hitdata('Ig-domains/hitdata.txt')
filter_fasta_sequences('sequence_results/cattle-sirpa_seq.faa', hit_dict, 'filtered_sequences.faa')
