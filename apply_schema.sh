#!/bin/bash

# dql
CMD="curl localhost:8080/alter?runInBackground=true -XPOST --data-binary '@schema_generated.dql' 2> /dev/null |jq '.data.code'|grep Success -q"

#graphql
#CMD="curl -X POST localhost:8080/admin/schema --data-binary '@schema_generated.graphql' --retry 10 --retry-delay 2 2> /dev/null |jq '.data.code'|grep Success -q"

while bash -c "$CMD"; [ $? = 1 ];
do echo "dgraph not ready, retry applying schema";
sleep 3;
done;
echo Schema applyed
