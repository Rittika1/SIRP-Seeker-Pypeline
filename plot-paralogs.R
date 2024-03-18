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

##-----Plotting the paralogs
plot_tree_barplot("paralogs/chicken-sirp-paralogs-species.nwk", "paralogs/chicken-sirp-paralogs.txt", "paralogs/chicken-sirp-paralog-output_plot.pdf")
plot_tree_barplot("paralogs/chicken-sirp-paralog-species.nwk", "paralogs/human-sirp-paralogs.txt", "paralogs/human-sirp-paralog-output_plot.pdf")
plot_tree_barplot("paralogs/cattle-sirp-paralogs-species.nwk", "paralogs/cattle-sirp-paralogs.txt", "paralogs/cattle-sirp-paralog-output_plot.pdf")

##----Plotting the Igdomain
plot_tree_barplot("paralogs/human-sirp-paralog-species.nwk", "Ig-domains/igdomain-count/human-igdomaincount.txt", "Ig-domains/igdomain-count/human-sirp-igdomain-output_plot.pdf")
plot_tree_barplot("paralogs/chicken-sirp-paralogs-species.nwk", "Ig-domains/igdomain-count/chicken-igdomaincount.txt", "Ig-domains/igdomain-count/chicken-sirp-igdomain-output_plot.pdf")
plot_tree_barplot("paralogs/cattle-sirp-paralogs-species.nwk", "Ig-domains/igdomain-count/cattle-igdomaincount.txt", "Ig-domains/igdomain-count/cattle-sirp-igdomain-output_plot.pdf")
