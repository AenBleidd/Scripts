#!/bin/bash

CWD=$(pwd)
LASTSAVEDREV=0
REVFILE="$CWD"/spelbuildbot.last
LOGFILE="$CWD"/spelbuildbot.log
USRFILE="$CWD"/spelbuildbot.usr
LOCKFILE="$CWD"/spelbuildbot.lock
BUILDFILE="$CWD"/spelbuild.sh

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
  echo -e "New pushed revisions:\n\n" > "$LOGFILE"
  hg log -r "$CURREV":"$LASTSAVEDREV" >> "$LOGFILE"
 
  if [ -f "$USRFILE" ]; then 
    while IFS='' read -r LINE || [[ -n "$LINE" ]]; do
      mutt -s "SPEL Build Bot: Mercurial Report" "$LINE" < "$LOGFILE"
    done < "$USRFILE"
  fi

  echo "$CURREV" > "$REVFILE"

  rm "$LOGFILE"
  cd "$CWD"
  /bin/bash "$BUILDFILE"
fi

rm -r "$LOCKFILE"

cd "$CWD"

