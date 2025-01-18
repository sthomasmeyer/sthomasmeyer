#!/bin/bash
# .github/date-management/bash-scripts/january/nba-all-star-game.sh

source .github/date-management/utilities/gen-notable-date-header.sh

output_file="README.md"
date="01-18"
image_path=".github/date-management/images/muhammad-ali-underwater.jpg"

# Generate the header
gen_notable_date_header "$date" "$output_file"

# Append custom content
{
    echo "![]($image_path)"
    echo ""
    echo "\"Float like a butterfly, sting like a bee; the hands can't hit what the eyes can't see.\" - Muhammad Ali"
} >> "$output_file"
