import os
from reader import read
from schema import create_schema
from rdf import create_rdf
from normalize_naming import normalize_data

path_to_data = os.environ.get('DATAPATH', 'data')

print("Reading CSVs")
data = read(version='v1.1', data_root_path='/Users/michaelhobbs/data/Adamant/refactored/grakn_ingest/')

print("Normalizing nodes and columns")
data = normalize_data(data)

print("Creating Schema")
create_schema(data, 'schema_generated.dql')
print("Creating RDF")
create_rdf(data, 'data.rdf')
end = time.time()
print(end - start)

