#!/bin/bash

# Create a folder named "proteomes" if it doesn't exist
mkdir -p proteomes

# Read the tab-separated file line by line
while IFS=$'\t' read -r name organism class taxon link proteome nb_proteins nb_character bps time; do
    # Skip the header line
    if [[ $name == "Common name" ]]; then
        continue
    fi

    # Construct the download URL
    download_url="https://rest.uniprot.org/uniprotkb/stream?format=fasta&query=%28%28proteome%3A$proteome%29%29"

    # Download the FASTA file and save it in the "proteomes" folder
    wget -O "proteomes/${organism}.fasta" "$download_url"

    # Optional: Add a delay to avoid overloading the server
    sleep 1

done < benchmark_data.tsv
