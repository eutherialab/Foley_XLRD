## step 2/2 to assign averaged ReLERNN derived recombination rates back to their genomic context
## This script takes the output of makeFullGenomeBedFile.sh 
## and assigns averaged ReLERNN recombination rates to their corresponding chromosomal position.
## run as python RecombRates2genome.py

import pandas as pd

# Set file names
file1 = "SampleRecomb_input.txt"
file2 = "output.txt"
output_file = "RecombMap2Genome_output.txt"

# Read in the averaged recombination rates
df1 = pd.read_csv(file1, sep="\t")

# Add a column called "lookup" to the table of averaged recombination rates with the concatenated values of Chr and Genome_coord
df1["lookup"] = df1["Chr"] + "_" + df1["Genome_coord"].astype(str)

# Read in the whole genome bedfile
df2 = pd.read_csv(file2, sep="\t")

# Add a column called "lookup" to the table of averaged recombination rates with the concatenated values of chromosome and window
df2["lookup"] = df2["chromosome"] + "_" + df2["start"].astype(str)

# Merge the two dataframes based on the "lookup" column and add the "rate" column from the table of averaged recombination rates to the whole-genome bedfile
df2 = pd.merge(df2, df1[["lookup", "rate"]], on="lookup", how="left")

# Write the output table
df2.to_csv(output_file, sep="\t", index=False)
