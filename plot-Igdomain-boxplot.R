library(phytools)
# ## simulate tree
# tree<-pbtree(n=26,tip.label=LETTERS[26:1])
# ## simulate species means
# x<-fastBM(tree)
# ## simulate individual samples, 5 per species
# xe<-sampleFrom(x,setNames(rep(0.5,Ntip(tree)),tree$tip.label),
#                setNames(rep(5,Ntip(tree)),tree$tip.label))
# round(xe,3)
# par(mfrow=c(1,2))
# plotTree(tree,mar=c(5.1,1.1,2.1,0.1))
# par(mar=c(5.1,0.1,2.1,1.1))
# boxplot(xe~factor(names(xe),levels=tree$tip.label),horizontal=TRUE,
#         axes=FALSE,xlim=c(1,Ntip(tree)))
# axis(1)
# title(xlab="log(body size)")


# # Read the file into a dataframe
# df <- read.table("", header = FALSE, stringsAsFactors = FALSE)
# Read the file into a dataframe, skipping the first 11 lines
# df <- read.table("~/Rittika-work/SIRPs_newdata/Ig-domains/human-sirpa_hitdata.txt", header = FALSE, stringsAsFactors = FALSE, skip = 11)

# Set the file path
# file_path <- "~/Rittika-work/SIRPs_newdata/Ig-domains/human-sirpa_hitdata.txt"

## Set the file path
file_path <- "/home/rittika/Rittika-work/SIRPs_newdata/Ig-domains/chicken-sirpa_hitdata.txt"
tree_path <- "/home/rittika/Rittika-work/SIRPs_newdata/paralogs/chicken-sirp-paralogs-species.nwk"
# Read the data from the file
data <- readLines(file_path)
vert_tree <- read.tree(tree_path)

# Filter for lines starting with "Q"
q_lines <- grep("^Q#", data, value = TRUE)

# Initialize an empty data frame to store the extracted data
extracted_data <- data.frame(Species = character(), `Hit.type` = character(), `NumOfIgDomains` = integer(), stringsAsFactors = FALSE)

# Iterate over each line and extract the relevant information
for (line in q_lines) {
  # Split the line into fields using a regular expression for spaces or tabs
  fields <- strsplit(line, "\\s+|\\t+")[[1]]
  
  # Extract the species name, hit type, and check if it's a superfamily
  species <- gsub(".*>([A-Za-z]+_[A-Za-z]+)_.*", "\\1", fields[3])
  hit_type <- fields[3]
  is_superfamily <- grepl("superfamily", line)
  
  # Check if the species and hit type combination already exists in the data frame
  existing_row <- which(extracted_data$Species == species & extracted_data$`Hit.type` == hit_type)
  
  if (length(existing_row) == 0) {
    # Add a new row to the data frame
    extracted_data <- rbind(extracted_data, data.frame(Species = species, `Hit.type` = hit_type, `NumOfIgDomains` = as.integer(is_superfamily)))
  } else {
    # Increment the number of Ig domains if it's a superfamily
    if (is_superfamily) {
      extracted_data$`NumOfIgDomains`[existing_row] <- extracted_data$`NumOfIgDomains`[existing_row] + 1
    }
  }
}

# Summarize the number of Ig domains per species and hit type
summary_table <- aggregate(`NumOfIgDomains` ~ Species + `Hit.type`, data = extracted_data, sum)

# # Print the summary table
# print(summary_table)

igdomaincount = summary_table$NumOfIgDomains
names(igdomaincount) = summary_table$Species
par(mfrow=c(1,2))
plotTree(vert_tree,mar=c(5.1,1.1,2.1,0.1))
par(mar=c(5.1,0.1,2.1,1.1))
boxplot(igdomaincount~factor(names(igdomaincount),levels=vert_tree$tip.label),horizontal=TRUE,
        axes=FALSE,xlim=c(1,Ntip(vert_tree)), col="salmon4")
axis(1)
title(xlab="chcken SIRP immunoglobulin domain count")
