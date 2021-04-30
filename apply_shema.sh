#!/bin/bash

while bash -c "curl -X POST localhost:8080/admin/schema --data-binary '@schema.graphql' --retry 10 --retry-delay 2 2> /dev/null |jq '.data.code'|grep Success -q"; [ $? = 1 ];
do echo "dgraph not ready, retry applying schema";
sleep 3;
done;
echo Schema applyed
