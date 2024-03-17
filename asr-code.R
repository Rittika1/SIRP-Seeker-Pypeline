library(phytools)
library(geiger)
library(ape)
packageVersion("phytools")

setwd("/home/rittika/Rittika-work/SIRPs_newdata/")

plot_ancestral_states <- function(newick_tree_file, paralog_count_file, output_pdf, plot_title) {
  # Read the Newick tree
  tree <- read.tree(file = newick_tree_file)
  tree$tip.label <- trimws(tree$tip.label)
  # Read the paralog count file
  paralog_counts <- read.table(paralog_count_file, header = FALSE, sep = "\t")
  colnames(paralog_counts) <- c("Species", "Count")
  paralog_counts$Species <- trimws(paralog_counts$Species)
  # Convert the data to a named vector
  count_vector <- setNames(paralog_counts$Count, paralog_counts$Species)
  
  # Perform ancestral state reconstruction
  reconstructed_states <- contMap(tree, count_vector, plot = FALSE)
  
  # Save the plot to a PDF
  pdf(file = output_pdf)
  plot(reconstructed_states, main = plot_title)
  dev.off()
}

plot_ancestral_states("paralogs/human-sirp-paralog-species.nwk", "paralogs/human-sirp-paralogs.txt", "paralogs/paralog-output_plot.pdf", "paralogs/Ancestral State Reconstruction SIRP paralog")
plot_ancestral_states("paralogs/human-sirp-paralog-species.nwk", "Ig-domains/igdomaincount/human-igdomaincount.txt", "Ig-domains/igdomaincount/paralog-output_plot.pdf", "Ig-domains/igdomaincount/Ancestral State Reconstruction Ig domains")
