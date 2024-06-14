#!/bin/bash

# Define the folder path (use the current directory if not specified)
folder_path="./"

# Find all .data files in the folder and rename them
find "$folder_path" -type f -name "*.data" | while read -r file; do
    date=$(date +"%Y-%m-%d")
    extension="${file##*.}"
    new_filename="${file%.*}_${date}.${extension}"

    echo "Renaming: $file into $new_filename"
    mv "$file" "$new_filename"
done
