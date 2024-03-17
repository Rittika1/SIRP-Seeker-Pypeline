library(phytools)
library(geiger)
library(ape)

setwd("/home/rittika/Rittika-work/SIRPs_newdata/")

plot_tree_barplot <- function(newick_tree_file, data_file, output_pdf) {
  # Read the Newick tree
  tree <- read.tree(file = newick_tree_file)
  
  # Read the data file
  data <- read.table(data_file, row.names = 1)
  colnames(data) <- c("Count")
  
  # Ensure that the tip labels and species names are correctly formatted
  tree$tip.label <- trimws(tree$tip.label)
  data$Species <- trimws(rownames(data))
  
  # Check the consistency between tree and data
  treedata(tree, data)
  
  # Save the plot to a PDF
  pdf(file = output_pdf)
  plotTree.barplot(tree, data, cex = 0.1)
  dev.off()
}

plot_tree_barplot("paralogs/human-sirp-paralog-species.nwk", "paralogs/human-sirp-paralogs.txt", "paralogs/human-sirp-paralog-output_plot.pdf")
plot_tree_barplot("paralogs/human-sirp-paralog-species.nwk", "Ig-domains/igdomaincount/human-igdomaincount.txt", "Ig-domains/igdomaincount/human-sirp-igdomain-output_plot.pdf")
