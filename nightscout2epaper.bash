#!/bin/bash
URL=https://YOURSITE.TLD/api/v1/entries/current.json
CURRDATE=$(date '+%s')
curl -s $URL |sed 's/,\"delta.*//' |sed -e 's/.*sgv\"://' > "value.txt"
curl -s $URL |sed -e 's/.*direction\":\"//' |sed 's/\",\"type.*//' > "direction.txt"
LASTVALUE=$(curl -s $URL |sed -e 's/.*date\"://'|cut -c -10)
DIFF=$((CURRDATE-LASTVALUE))
DIFF=$((DIFF/60))
LASTDATE=$(date -d @$LASTVALUE +%H:%M)
echo "Vor" $DIFF "Min um" $LASTDATE > "timeinfo.txt"
if [ $DIFF -gt 10 ]; then echo 1 > "old.txt"; else echo 0 > "old.txt"; fi
python2 nightscout.py
