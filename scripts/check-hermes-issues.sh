#!/bin/bash
# Check Hermes Agent issues for closure
# Run daily via cron: 0 9 * * * ~/.openclaw/workspace-genesis/scripts/check-hermes-issues.sh >> ~/.openclaw/hermes-tracker.log 2>&1

GH_TOKEN=$(gh auth token 2>/dev/null)
TRACKER=~/.openclaw/workspace-genesis/memory/hermes-tracker.yml

for issue in 342 514; do
  state=$(gh api repos/NousResearch/hermes-agent/issues/$issue --jq '.state' 2>/dev/null)
  if [ "$state" = "closed" ]; then
    # Check if we already notified
    notified=$(grep -A2 "number: $issue" $TRACKER | grep notification_sent | awk '{print $3}')
    if [ "$notified" = "false" ]; then
      title=$(gh api repos/NousResearch/hermes-agent/issues/$issue --jq '.title' 2>/dev/null)
      msg="🚨 Hermes Agent #${issue} CLOSED: ${title}"
      # Update tracker
      sed -i "s/notification_sent: false/notification_sent: true/" $TRACKER
      echo "$(date): $msg"
      # Notify via OpenClaw session (write to notify file for next heartbeat)
      echo "$msg" >> ~/.openclaw/hermes-issue-alert.txt
    fi
  fi
done