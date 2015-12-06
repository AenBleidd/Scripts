#!/bin/bash

CWD=$(pwd)
LASTSAVEDREV=0
REVFILE="$CWD"/spelbuildbot.last
LOGFILE="$CWD"/spelbuildbot.log
USRFILE="$CWD"/spelbuildbot.usr
LOCKFILE="$CWD"/spelbuildbot.lock

if mkdir "$LOCKFILE"; then
  echo "Start SPEL Build Bot"
else
  exit 1
fi

if [ -f "$REVFILE" ]; then
  LASTSAVEDREV=$(cat "$REVFILE")
fi

cd /srv/pose/

[[ $(hg log -l 1) =~ changeset:[[:space:]]*([0-9]{1}+): ]]
CURREV=${BASH_REMATCH[1]}

if [ "$CURREV" -gt "$LASTSAVEDREV" ]; then
  echo -e "Last pushed revisions:\n\n" > "$LOGFILE"
  hg log -r "$CURREV":"$LASTSAVEDREV" >> "$LOGFILE"
  
  while IFS='' read -r LINE || [[ -n "$LINE" ]]; do
    mutt -s "SPEL Build Bot Report" "$LINE" < "$LOGFILE"
  done < "$USRFILE"

  echo "$CURREV" > "$REVFILE"

  rm "$LOGFILE"
fi

rm -r "$LOCKFILE"

