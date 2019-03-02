#!/bin/bash
URL=https://YOURSITE.TLD/api/v1/entries/current.json
CURRDATE=$(date '+%s')
if [ -f lasthour.txt ];
        then LASTHOUR=$(cat lasthour.txt);
        else LASTHOUR=0;
fi
curl -s $URL |sed 's/,\"delta.*//' |sed -e 's/.*sgv\"://' > "value.txt"
curl -s $URL |sed -e 's/.*direction\":\"//' |sed 's/\",\"type.*//' > "direction.txt"
LASTVALUE=$(curl -s $URL |sed -e 's/.*date\"://'|cut -c -10)
DIFF=$((CURRDATE-LASTVALUE))
DIFF=$((DIFF/60))
DIFFH=$((DIFF/60))
LASTDATE=$(date -d @$LASTVALUE +%H:%M)
if [ $DIFF -gt 10 ]; then echo 1 > "old.txt"; else echo 0 > "old.txt"; fi

if [ $DIFF -lt 60 ]; then
        echo "Vor" $DIFF "Min um" $LASTDATE > "timeinfo.txt"
        python2 nightscout.py;
else
        if [ $DIFFH -gt $LASTHOUR ]; then
                echo "Vor" $DIFFH "Stunden um" $LASTDATE > "timeinfo.txt"
                python2 nightscout.py;
        fi
fi
echo $DIFFH > "lasthour.txt"
