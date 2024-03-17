from ete3 import Tree

# Load the tree
tree = Tree("/home/rittika/Rittika-work/SIRPs_newdata/Ig-domains/trimmed-aliview/cattle-sirpa_hitdata_aligned_trimmed_merged_aligned.faa.treefile")


# Function to extract the species name from the leaf node name
def get_species_name(leaf_name):
    parts = leaf_name.split("_")
    return "_".join(parts[:2])  # Adjust this based on your naming convention

# Function to prune duplicates within each clade
def prune_duplicates(node):
    species_dict = {}
    for leaf in node.iter_leaves():
        species_name = get_species_name(leaf.name)
        if species_name not in species_dict:
            species_dict[species_name] = leaf.name
        else:
            # Remove the duplicate leaf
            leaf.detach()

    # Recursively prune duplicates in child nodes
    for child in node.children:
        prune_duplicates(child)

# Start pruning from the root of the tree
prune_duplicates(tree)

# Check for empty node names and assign a placeholder if necessary
for node in tree.traverse():
    if not node.name:
        node.name = "Placeholder"

tree.write(outfile="/home/rittika/Rittika-work/SIRPs_newdata/Ig-domains/nodups-perclade/pruned_tree.nwk")
