#!/bin/bash

# Directory to process (change as needed or pass as $1)
DIR="."

# Loop over all files (not directories) in the given directory
for INPUT in "$DIR"/*; do
    # Only process regular files
    [ -f "$INPUT" ] || continue

    # Get base name and extension
    BASENAME="${INPUT##*/}"
    EXT="${BASENAME##*.}"
    FILENAME="${BASENAME%.*}"

    # Output file: add _modified before extension
    OUTPUT="$DIR/${FILENAME}_modified.${EXT}"

    # Extract method name from Name: section, trim, replace spaces with underscores
    METHOD_NAME=$(awk '/^Name:/{getline; gsub(/^[ \t"]+|[ \t"]+$/, "", $0); print; exit}' "$INPUT")
    METHOD_NAME_UNDERSCORE="${METHOD_NAME// /_}"

    # Escape for sed (slashes, ampersands)
    METHOD_NAME_ESCAPED=$(printf '%s' "$METHOD_NAME_UNDERSCORE" | sed 's/[\/&]/\\&/g')

    # Replace all SAMPL8-XX_extraNNN with SAMPL8-XX_<name>_extraNNN
    sed -E "s/(SAMPL8-[0-9]+)_extra([0-9]+)/\1_${METHOD_NAME_ESCAPED}_extra\2/g" "$INPUT" > "$OUTPUT"

    echo "Processed $INPUT -> $OUTPUT"
done

