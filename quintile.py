## This script takes the output from normalize.py as input
## and assigns then to a quintile value corresponding to high and low recombination quintiles.
## In this way the conservation of rates between species can be indirectly compared.

import pandas as pd
import argparse
import sys

def assign_quintiles(input_file, output_file):
    try:
        df = pd.read_csv(input_file, delimiter='\t')
        
        if df.empty:
            print("Error: The input file is empty.")
            sys.exit(1)
        
        if len(df.columns) < 5:
            print("Error: The input file does not have at least 5 columns.")
            sys.exit(1)

        df.columns = df.columns.str.strip()
        fifth_col = df.columns[4] 

        if not pd.api.types.is_numeric_dtype(df[fifth_col]):
            print(f"Error: The 5th column '{fifth_col}' does not contain numeric data.")
            sys.exit(1)

        valid_data = df[fifth_col].dropna()
        if valid_data.empty:
            print(f"Error: The 5th column '{fifth_col}' contains only NaNs.")
            sys.exit(1)

        df['Quintile'] = pd.qcut(valid_data, 5, labels=False, duplicates='drop') + 1

        df.loc[valid_data.index, 'Quintile'] = pd.qcut(valid_data, 5, labels=False, duplicates='drop') + 1

        df.to_csv(output_file, sep='\t', index=False)
        print(f"Successfully saved the output to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Assign quintiles to the 5th column of a tab-delimited file and save the result to a new file.")
    parser.add_argument('input_file', type=str, help='Path to the input tab-delimited file')
    parser.add_argument('output_file', type=str, help='Path to the output tab-delimited file')
    
    args = parser.parse_args()
    
    assign_quintiles(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
