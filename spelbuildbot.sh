#!/bin/bash

CWD=$(pwd)
LASTSAVEDREV=0
REVFILE=/home/vkoshura/spelbuildbot.last
LOGFILE=/home/vkoshura/spelbuildbot.log
USRFILE=/home/vkoshura/spelbuildbot.usr
LOCKFILE=/home/vkoshura/spelbuildbot.lock
BUILDFILE=/home/vkoshura/spelbuild.sh

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
  LASTSAVEDREV=$((LASTSAVEDREV+1))
  echo -e "New pushed revisions:\n\n" > "$LOGFILE"
  hg log -r "$CURREV":"$LASTSAVEDREV" >> "$LOGFILE"
 
  if [ -f "$USRFILE" ]; then 
    while IFS='' read -r LINE || [[ -n "$LINE" ]]; do
      mutt -s "SPEL Build Bot: Mercurial Report" "$LINE" < "$LOGFILE"
    done < "$USRFILE"
  fi

  echo "$CURREV" > "$REVFILE"

  rm "$LOGFILE"
  su -c "$BUILDFILE" -s /bin/bash vkoshura
fi

rm -r "$LOCKFILE"

cd "$CWD"

