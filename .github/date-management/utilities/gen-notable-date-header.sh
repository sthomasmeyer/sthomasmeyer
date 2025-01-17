#!/bin/bash
# .github/date-management/utilities/gen-notable-date-header.sh

fetch_title() {
  local date=$1
  local config_file=".github/date-management/notable-dates.yml"

  if [ -z "$date" ]; then
    echo "Error: Date parameter is required" >&2
    return 1
  fi

  local title=$(yq ".dates.[\"$date\"].title" "$config_file")

  if [ -z "$title" ] || [ "$title" == "null" ]; then
    echo "Error: No title found for date $date" >&2
    return 1
  fi

  echo "$title"
}

gen_notable_date_header() {
  local date=$1
  local output_file=${2:-"README.md"}

  local title=$(fetch_title "$date")
  if [ $? -ne 0 ]; then
    echo "Error generating header for date $date" >&2
    return 1
  fi

  {
    echo "# ${title}"
    echo ""
    echo "_Updated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')_"
    echo ""
  } > "$output_file"
}
