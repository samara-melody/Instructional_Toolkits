#!/bin/bash

# Folder containing .su files
input_dir="./data_preprocessed/allshots"

# Loop over all .su files in the folder
for sufile in "$input_dir"/*.su; do
    # Get base name without extension
    base=$(basename "$sufile" .su)
    
    # Set output SEGY filename
    outfile="$input_dir/${base}.sgy"
    
    # Convert SU to SEGY
    segyhdrs < "$sufile"
    segywrite < "$sufile" tape="$outfile"
    
    echo "Converted $sufile -> $outfile"
done

rm ./header
rm ./binary