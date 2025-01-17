#!/bin/bash
# .github/date-management/bash-scripts/january/nba-all-star-game.sh

source .github/date-management/utilities/gen-notable-date-header.sh

output_file="README.md"
date="01-17"

# Generate the header
gen_notable_date_header "$date" "$output_file"

# Append custom content
{
    echo "On this day, in 1961, Oscar Robertson made history as the youngest NBA All-Star."
    echo ""
    echo "Some notable achievements from this game:"
    echo "- Robertson scored 23 points"
    echo "- The West defeated the East, 153-131"
    echo "- The game was played at the Onondaga County War Memorial"
} >> "$output_file"
