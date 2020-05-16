#!/bin/sh

# GNU parallel use to make sure both keep running
cat <<EOF | parallel --halt now,fail=1  
echo 'Running Backend'; cd data && python myserver.py; exit 0
echo 'Running UI'; npm start; exit 0
EOF
echo "One of the two servers failed"
