#!/bin/bash
# .github/date-management/bash-scripts/january/nba-allstar-game.sh

TITLE=$(yq ".dates.['01-17'].title" ../../notable-dates.yml)

{
    echo "# ${TITLE}"
    echo ""
    echo "_Updated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')_"
    echo ""
    echo "On this day, in 1961, Oscar Robertson made history as the youngest NBA All-Star."
    echo ""
    echo "Some notable achievements from this game:"
    echo "- Robertson scored 23 points"
    echo "- The West defeated the East, 153-131"
    echo "- The game was played at the Onondaga County War Memorial"
} > README.md