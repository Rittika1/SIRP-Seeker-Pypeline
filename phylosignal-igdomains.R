##--This code will take in a Ig domains file made using NCBI CDD 
##-- Input a tree file and calculate phylogenetic signal

# Load the necessary library
library(ggplot2)
library(viridis)
library(grid)
library(gridExtra)
library(phytools)
library(geiger)

##Input Files
file_path <- "~/Rittika-work/SIRPs_newdata/Ig-domains/cattle-sirpa_hitdata.txt"
vert_tree_path<- "~/Rittika-work/SIRPs_newdata/Ig-domains/cattlesirpa_species_output.nwk"

output_path <- "~/Rittika-work/SIRPs_newdata/Ig-domains/cattlesirpa_species_output.txt"

calculate_ig_domains <- function(file_path, output_path) {
  # Read the data from the file
  data <- readLines(file_path)
  
  # Filter for lines containing "superfamily"
  superfamily_lines <- grep("superfamily", data, value = TRUE)
  
  # Initialize an empty data frame to store the extracted data
  extracted_data <- data.frame(Query = character(), `Hit.type` = character(), stringsAsFactors = FALSE)
  
  # Iterate over each line and extract the relevant information
  for (line in superfamily_lines) {
    # Split the line into fields using a regular expression for spaces or tabs
    fields <- strsplit(line, "\\s+|\\t+")[[1]]
    
    # Extract the query and hit type
    query <- fields[1]
    hit_type <- gsub(">", "", fields[3])
    
    # Add the extracted data to the data frame
    extracted_data <- rbind(extracted_data, data.frame(Query = query, `Hit.type` = hit_type))
  }
  
  # Extract species names from the Query column
  extracted_data$Species <- sapply(strsplit(extracted_data$Hit.type, split = "_"), function(x) paste(x[1], x[2], sep = "_"))
  
  # Count the number of Ig domains per species
  ig_domain_counts <- table(extracted_data$Species)
  
  # Convert the table to a data frame
  ig_domain_df <- as.data.frame(ig_domain_counts)
  colnames(ig_domain_df) <- c("Species", "NumIgDomains")
  
  # Write the Species column to a file
  write.table(ig_domain_df$Species, file = output_path, row.names = FALSE, col.names = FALSE, quote = FALSE)
  
  # Return the final data frame
  return(ig_domain_df)
}

##Read in data from the input files
vert_tree <- read.tree(vert_tree_path)
final_df <- calculate_ig_domains(file_path, output_path)



##--Steps to calculate phylogentic signal
num_Igdomains <- final_df$NumIgDomains
names(num_Igdomains) <- final_df$Species

treedata(vert_tree, num_Igdomains)

##-----ktest
k.test.igdomains <- phylosig(vert_tree, num_Igdomains, method = "K", test = TRUE, nsim = 10000)
print(paste("Blomberg's K value is: ", k.test.igdomains$K))

##----lambda 
lambda.test.igdomains <- phylosig(vert_tree, num_Igdomains, method = "lambda", test = TRUE)
print(paste("Lambda value is: ", lambda.test.igdomains$lambda))


# print(final_df)
