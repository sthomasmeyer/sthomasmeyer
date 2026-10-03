#!/bin/bash
# .github/date-management/render-notable-date.sh
# Checks if today is a notable date, and if so, renders either its custom narrative
# or a fallback header & description into the target staging file.

set -eo pipefail

CURRENT_DATE=$(date -u '+%m-%d')
CONFIG_FILE=".github/date-management/notable-dates.yml"
OUTPUT_FILE="${1:-${TARGET_FILE:-README.md}}"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: Configuration file not found at $CONFIG_FILE" >&2
    exit 1
fi

# Query today's entry once as a JSON object using yq
ENTRY=$(yq -o=json ".dates.[\"$CURRENT_DATE\"] // empty" "$CONFIG_FILE" 2>/dev/null || true)

if [[ -z "$ENTRY" || "$ENTRY" == "null" ]]; then
    echo "Notice: Today ($CURRENT_DATE) is not a designated notable date."
    if [[ -n "$GITHUB_OUTPUT" ]]; then
        echo "is_notable_date=false" >> "$GITHUB_OUTPUT"
    fi
    exit 0
fi

# Extract fields from the single JSON object
TITLE=$(echo "$ENTRY" | jq -r '.title // empty')
DESCRIPTION=$(echo "$ENTRY" | jq -r '.description // empty')
SCRIPT=$(echo "$ENTRY" | jq -r '.bash_script // empty')

# Export for GitHub Actions downstream steps (e.g. commit messages)
if [[ -n "$GITHUB_OUTPUT" ]]; then
    echo "is_notable_date=true" >> "$GITHUB_OUTPUT"
    echo "title=$TITLE" >> "$GITHUB_OUTPUT"
fi

# Render narrative script or fallback content
SCRIPT_PATH=".github/date-management/bash-scripts/$SCRIPT"

if [[ -n "$SCRIPT" && "$SCRIPT" != "null" && -f "$SCRIPT_PATH" ]]; then
    echo "Executing custom narrative script: $SCRIPT_PATH"
    chmod +x "$SCRIPT_PATH"
    "$SCRIPT_PATH" "$OUTPUT_FILE"
else
    echo "Rendering fallback notable date content for: $TITLE"
    {
        echo "# ${TITLE}"
        echo ""
        echo "_Updated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')_"
        echo ""
        if [[ -n "$DESCRIPTION" ]]; then
            echo "${DESCRIPTION}"
            echo ""
        fi
    } >> "$OUTPUT_FILE"
fi