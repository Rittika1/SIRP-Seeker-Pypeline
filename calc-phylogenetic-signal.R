library(phytools)

calculate_phylogenetic_signal <- function(tree, table, label) {
  # Extract the second column and set its names to the first column
  trait_vector <- table[,2]
  names(trait_vector) <- table[,1]
  
  # Calculate Blomberg's K
  k_test <- phylosig(tree, trait_vector, method = "K", test = TRUE, nsim = 10000)
  cat("Blomberg's K value for", label, "is:", k_test$K, "\n")
  cat("p-value for Blomberg's K of", label, "is:", k_test$P, "\n")
  
  # Calculate Pagel's lambda
  lambda_test <- phylosig(tree, trait_vector, method = "lambda", test = TRUE)
  cat("Lambda value for", label, "is:", lambda_test$lambda, "\n")
  cat("p-value for Lambda of", label, "is:", lambda_test$P, "\n")
}

# Example usage:
# vert_tree <- read.tree("path/to/your/tree/file")
# table <- read.table("path/to/your/table/file", header = TRUE)
# calculate_phylogenetic_signal(vert_tree, table, "human-sirp-paralog")

##--for SIRP paralog
setwd("~/Rittika-work/SIRPs_newdata/phylogenetic-signal")

##----human SIRP
vert_tree <- read.tree("human-sirp-paralog-species.nwk")
table <- read.table("human-sirp-paralogs.txt", header = FALSE)
calculate_phylogenetic_signal(vert_tree, table, "chicken-sirp-paralog")

##----chicken SIRP
vert_tree <- read.tree("chicken-sirp-paralogs-species.nwk")
table <- read.table("chicken-sirp-paralogs.txt", header = FALSE)
calculate_phylogenetic_signal(vert_tree, table, "chicken-sirp-paralog")

##----cattle SIRP
vert_tree <- read.tree("cattle-sirp-paralogs-species.nwk")
table <- read.table("cattle-sirp-paralogs.txt", header = FALSE)
calculate_phylogenetic_signal(vert_tree, table, "cattle-sirp-paralog")

##--For Ig domains
# setwd("~/Rittika-work/SIRPs_newdata/Ig-domains")

##----human Ig domains
vert_tree <- read.tree("human-sirp-paralog-species.nwk")
table <- read.table("human-igdomaincount.txt", header = FALSE)
calculate_phylogenetic_signal(vert_tree, table, "human-sirp-igdomains")

##----chicken Ig domains
vert_tree <- read.tree("chicken-sirp-paralogs-species.nwk")
table <- read.table("chicken-igdomaincount.txt", header = FALSE)
calculate_phylogenetic_signal(vert_tree, table, "chicken-sirp-Igdomains")

##----cattle Ig domains
vert_tree <- read.tree("cattle-sirp-paralogs-species.nwk")
table <- read.table("cattle-igdomaincount.txt", header = FALSE)
calculate_phylogenetic_signal(vert_tree, table, "cattle-sirp-Igdomains")


