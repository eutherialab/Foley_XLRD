# Foley_XLRD
This repository contains code associated with the publication titled "An ancient X chromosome recombination desert acts as a supergene in placental mammals."

These are a series of helper scripts to manipulate the bscorrected recombination rates output from ReLERNN (https://github.com/kr-colab/ReLERNN) 

Scripts are written in bash, perl and python3. Python scripts require the following dependencies:
pandas, csv, argparse & sys

**Assessing the conservation of historical, long-term recombination rates.**

First, raw bscorrected recombination rates output from ReLERNN are averaged in 2Mb windows with a 50kb step. Averaging rates in large blocks enables assessments of long-term historical recombination rates as opposed to recent differences that can occur between species, populations, individuals, and sexes.

Run as 

_perl relernn_sliding_average.pl_

replace DATAFILE with the raw bscorrected output from ReLERNN. As written, the script averages recombination rates in 2Mb blocks with a step of 50kb. Change hard-coded numbers as required to vary block and window size.

**Restoring genomic context.**

The raw output omits windows for which there was insufficient data to infer a recombination rate. Therefore, data cannot be plotted directly and must be put back into its genomic context. This is achieved in two steps. First, taking a bedfile of chromosome names and lengths (RecombRates2genome_SampleBed.bed), a whole-genome bedfile comprising coordinates for 50kb windows is generated using

_bash makeFullGenomeBedFile.sh _

Then run 

_python RecombRates2genome.py_

This script takes the output of makeFullGenomeBedFile.sh and assigns averaged ReLERNN recombination rates to their corresponding chromosomal position.

**Indirect comparisons of recombination landscapes for species with unknown or different mutation rates.**

To indirectly compare the recombination landscape of orthologous chromosomes across different species, first, all recombination rates across a chromosome are normalized to the largest value (where the largest value is assigned a value of 1). For a given chromosome (Sample_normalize_input.txt) run the script as follows:

_python normalize.py  <input_file> <output_file> <column_index> <normalized_column_name>_

Where <input file> corresponds to the path to input in the form of Sample_normalize_input.txt,
output file specifies the path to the desired output file,
column index refers to the column that contains recombination rates to be normalized - NOTE - python starts counting at 0,
and where normalized_column_name is the desired name of the new column where the normalized rates will be written.

Then, using the output from the previous script as input rates are assigned to recombination quintiles (this can be changed) using 

_python normalize.py <input_file> <output_file>_

Quintile assignments are output in a column in the output file. In this way, relative rates of recombination across an orthologous chromosome can be indirectly compared across species.
