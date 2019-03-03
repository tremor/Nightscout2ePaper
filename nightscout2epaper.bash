#!/bin/bash
SERVER=SERVERNAME.OF.YOUR.NIGHTSCOUT.INSTANCE
SECRET=API_SECRET
PING=$SERVER #or use www.google.com if your server is not pingable
#PING=www.google.com
SECRETSHA1=$(echo -n $SECRET | sha1sum | awk '{print $1}')
URL="-s --header API-SECRET:"$SECRETSHA1" https://"$SERVER"/api/v1/entries/current.json"
ping -q -c5 $PING > /dev/null
if [ $? -eq 0 ];
        then
        CURRDATE=$(date '+%s')
        if [ -f lasthour.txt ];
                then LASTHOUR=$(cat lasthour.txt);
                else LASTHOUR=0;
        fi
        curl $URL | sed -e 's/.*sgv\"://' | sed 's/,\".*//' > "value.txt"
        curl $URL | sed -e 's/.*direction\":\"//' | sed 's/\",\".*//' > "direction.txt"
        LASTVALUE=$(curl $URL | sed -e 's/.*date\"://'|cut -c -10)
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
        echo $DIFFH > "lasthour.txt";
else
        echo No Connection;
fi
