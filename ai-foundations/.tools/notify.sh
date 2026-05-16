#!/bin/bash
# Daily 11am nudge for the AI lesson. Fired by launchd.
# Uses a modal dialog (not a Notification Center notification) because macOS
# Sequoia silently drops osascript notifications when no notifier app is
# registered. A dialog always appears and needs no notification permission.
# The /lesson command self-bootstraps the day's lesson, so this only reminds.

DIR="/Users/ginagu/Documents/GitHub/Courses/ai-foundations"

CHOICE=$(osascript <<EOF 2>>"$DIR/.tools/notify.log"
set q to button returned of (display dialog "Time for your daily AI lesson — about an hour, one concept at a time. You've got this." with title "🧠 AI Lesson Time" buttons {"Later", "Open Terminal here"} default button "Open Terminal here" with icon note)
return q
EOF
)

if [ "$CHOICE" = "Open Terminal here" ]; then
  open -a Terminal "$DIR"
fi
