#!/bin/bash
# Script to dismiss all warning-level alerts

# List of alert numbers to dismiss
ALERT_NUMBERS="10 14 15 185 195 196 197 200 203 209 219 220 221 224 227 233 3 5 6 7 8 9"

# Reason for dismissal
REASON="won't fix"
COMMENT="Dismissing warning-level alert as per request"

# Loop through each alert number and dismiss it
for alert in $ALERT_NUMBERS; do
  echo "Dismissing alert #$alert..."
  gh api --method PATCH /repos/thomasvincent/python-network-discovery-tool/code-scanning/alerts/$alert \
    -f state=dismissed \
    -f dismissed_reason="$REASON" \
    -f dismissed_comment="$COMMENT"
  
  # Add a small delay to avoid rate limiting
  sleep 1
done

echo "All warning-level alerts have been dismissed."
