#!/bin/bash
# .github/date-management/bash-scripts/january/obama-inauguration-day.sh

source .github/date-management/utilities/gen-notable-date-header.sh

output_file="README.md"
date="01-20"
image_path=".github/date-management/bash-scripts/january/images/barack-obama.webp"

gen_notable_date_header "$date" "$output_file"

{
  echo "![]($image_path)"
  echo ""
} >> "$output_file"
