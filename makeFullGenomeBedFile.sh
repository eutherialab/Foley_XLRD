#!/bin/bash

## This script takes as input a bedfile of per chromosome genome coordinates e.g. RecombRates2genome_SampleBed.txt
## and generates a corresponding bedfile for the genome in 50kb windows(can change).
## run as bash makeFullGenomeBedFile.sh
## step 1/2 to assign averaged ReLERNN derived recombination rates back to their genomic context
## step 2/2 is RecombRates2genome.py

# Set the input bedfile name
bed_file="SampleBed.bed"

# Set the output file name - don't change
output_file="RecombRates2genome_SampleBed.txt"

# Open the output file
echo "chromosome	start	end" > "$output_file"

# Read in each line of the bed file
while read -r line; do
  # Extract the chromosome, start, and end positions from the line
  chromosome=$(echo "$line" | cut -f 1)
  start=$(echo "$line" | cut -f 2)
  end=$(echo "$line" | cut -f 3)

  # Set the window size the recombination rates were averaged in e.g. 50kb - window start should be window size -1
  num_windows=$((($end - $start) / 50000))

  for i in $(seq 0 $num_windows); do
    window_start=$(( $start + ($i * 50000) ))
    window_end=$(( $window_start + 49999 ))

    # Write output
    echo "$chromosome	$window_start	$window_end" >> "$output_file"
  done
done < "$bed_file"
