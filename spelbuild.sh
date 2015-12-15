#!/bin/bash

CWD=$(pwd)
LOGFILE=/home/vkoshura/spelbuild.log
TESTSFILE=/home/vkoshura/spelbuildtests.log
USRFILE=/home/vkoshura/spelbuildbot.usr
LOCKFILE=/home/vkoshura/spelbuild.lock
ERRORFLAG=0

if mkdir "$LOCKFILE"; then
  echo "Start SPEL Build"
else
  exit 1
fi

cd /home/vkoshura/pose/

echo -e "Start build:\n\n" > "$LOGFILE"

hg pull &>> "$LOGFILE"
if [ $? -eq 0 ]; then
  hg up &>> "$LOGFILE"
  if [ $? -eq 0 ]; then
    cd build
    make clean &>> "$LOGFILE"
    if [ $? -eq 0 ]; then
      cmake ../src/ &>> "$LOGFILE"
      if [ $? -eq 0 ]; then
        make -j2 &>> "$LOGFILE"
        if [ $? -eq 0 ]; then
          cd tests
          ./speltests &> "$TESTSFILE"
        else
          ERRORFLAG=4
        fi
      else
        ERRORFLAG=3
      fi
    else
      ERRORFLAG=2
    fi
  else
    ERRORFLAG=1
  fi
else
  ERRORFLAG=1
fi

if [ "$ERRORFLAG" -eq 0 ]; then
  STATUS="SUCCESSFULL"
elif [ "$ERRORFLAG" -eq 1 ]; then
  STATUS="FAILED: Repository update failed"
elif [ "$ERRORFLAG" -eq 2 ]; then
  STATUS="FAILED: Clean failed"
elif [ "$ERRORFLAG" -eq 3 ]; then
  STATUS="FAILED: CMake rebuild failed"
elif [ "$ERRORFLAG" -eq 4 ]; then
  STATUS="FAILED: SPEL rebuild failed"
else
  STATUS="FAILED: Unknown reason"
fi

if [ "$ERRORFLAG" -eq 0 ]; then
  if [ -f "$TESTSFILE" ]; then
    if [ -f "$USRFILE" ]; then 
      while IFS='' read -r LINE || [[ -n "$LINE" ]]; do
        echo "Build complete" | mutt -a "$LOGFILE" "$TESTSFILE" -s "SPEL Build Bot: Build Report: $STATUS" -- "$LINE"
      done < "$USRFILE"
    fi
  else
    if [ -f "$USRFILE" ]; then 
      while IFS='' read -r LINE || [[ -n "$LINE" ]]; do
        echo "Tests log is not present" | mutt -a "$LOGFILE" -s "SPEL Build Bot: Build Report: $STATUS" -- "$LINE"
      done < "$USRFILE"
    fi
  fi
else
  if [ -f "$USRFILE" ]; then 
    while IFS='' read -r LINE || [[ -n "$LINE" ]]; do
      echo "Tests log is not present" | mutt -a "$LOGFILE" -s "SPEL Build Bot: Build Report: $STATUS" -- "$LINE"
    done < "$USRFILE"
  fi
fi

rm "$LOGFILE"
rm "$TESTSFILE"
rm -r "$LOCKFILE"

cd "$CWD"

