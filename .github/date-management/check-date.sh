#!/bin/bash
# .github/date-management/check-date.sh

check_date() {
    CURRENT_DATE=$(date -u '+%m-%d')
    CONFIG_FILE=".github/date-management/notable-dates.yml"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Error: Configuration file not found at $CONFIG_FILE"
        exit 1
    fi
    
    if yq -e ".dates.[\"$CURRENT_DATE\"]" "$CONFIG_FILE" > /dev/null 2>&1; then
        echo "is_notable_date=true"
        echo "current_date=$CURRENT_DATE"
        
        TITLE=$(yq ".dates.[\"$CURRENT_DATE\"].title" "$CONFIG_FILE")
        DESCRIPTION=$(yq ".dates.[\"$CURRENT_DATE\"].description" "$CONFIG_FILE")
        
        echo "title=$TITLE"
        echo "description=$DESCRIPTION"
        return 0
    else
        # Not a special date
        echo "is_notable_date=false"
        return 1
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    check_date
fi