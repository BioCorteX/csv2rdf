import os
from reader import read
from schema import create_schema
from rdf import create_rdf
from normalize_naming import normalize_data
import time

start = time.time()

path_to_data = os.environ.get('DATAPATH', 'data')

print("Reading CSVs")
data = read(version='', data_root_path='/Users/michaelhobbs/data/')

print("Normalizing nodes and columns")
data = normalize_data(data)

print("Creating Schema")
create_schema(data, 'schema_generated.dql')
print("Creating RDF")
create_rdf(data, 'data.rdf')
end = time.time()
print(end - start)

