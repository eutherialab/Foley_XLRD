## This script takes averaged per chromosome recombination rates (Sample_normalize_input.txt) as input
## The script normalizes all values to the highest recombintion rate across the chromosome e.g. the highest 
## recombination rate is assigned a value of 1. This allows for indirect comparisons of recombination patterns
## among orthologous chromosomes between species
## run as 
## python normalize.py <input_file> <output_file> <column_index> <normalized_column_name>
## Where input file corresponds to the path to input in the form of Sample_normalize_input.txt
## output file specifices the path to the desired output file
## column index refers to the column which contains recombination rates to be normalized
## NOTE - python starts counting at 0
## and where normalized_column_name is the desired name of the new column where the normalized rates will be written.

import csv
import argparse

def add_normalized_column(input_file, output_file, column_index, normalized_column_name):
    with open(input_file, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        data = list(reader)

    column_values = []
    for row in data[1:]:  # Exclude header
        try:
            column_values.append(float(row[column_index]))
        except ValueError:
            column_values.append(None)

    valid_values = [val for val in column_values if val is not None]

    # Find the min and max values in the column
    min_value = min(valid_values)
    max_value = max(valid_values)

    # Normalize the column values
    normalized_values = [(val - min_value) / (max_value - min_value) if val is not None else '' for val in column_values]

    data[0].append(normalized_column_name)

    for i, row in enumerate(data[1:]):
        row.append(normalized_values[i])

    with open(output_file, 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerows(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize a column in a tab-delimited file and add it as a new column.")
    parser.add_argument('input_file', help="Path to the input tab-delimited file")
    parser.add_argument('output_file', help="Path to the output tab-delimited file")
    parser.add_argument('column_index', type=int, help="Index of the column to normalize (0-based)")
    parser.add_argument('normalized_column_name', help="Name for the new normalized column")

    args = parser.parse_args()

    add_normalized_column(args.input_file, args.output_file, args.column_index, args.normalized_column_name)

    print(f"Normalized data has been added to {args.output_file}")
