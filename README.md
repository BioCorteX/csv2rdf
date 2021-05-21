CSV2RDF

```
make setup-pipenv
```

make sure you have docker on your machine.

download and unzip the graph data from (get the latest version) https://console.cloud.google.com/storage/browser/biocortex_datasets/POC_Final_Data?authuser=0&supportedpurview=project&pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&prefix=&forceOnObjectsSortingFiltering=false


update the data directory location in ```src/create_rdf.py``` line 9.

run the following commands

```
make create_rdf
make import-bulk
```

open a google chrome and go to https://play.dgraph.io/?latest and connect to http://localhost:8080 by clicking on the Dgraph Server Connection button on the top left.