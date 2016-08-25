#!/bin/bash
cd /root/rt-git/holyoke/mghpcc_rack_plotting/current_tables
\cp -f * /root/prev-tables
git pull origin master
cd /root/rt-change
file=*update-csv.txt
\rm -f $file
python update.py
FILES=/root/rt-change/*-update-csv.txt
if [ -e $FILES ]
then
	for f in $FILES; do  wget --delete-after -q --user=admin --password=password --post-data="csv_text=$(cat $f)" "http://172.16.1.234/racktables/index.php?module=redirect&page=import&tab=default&op=importData"; done

fi
