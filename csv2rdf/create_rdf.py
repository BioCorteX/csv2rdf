import os
from reader import read
from schema import create_schema
from rdf import create_rdf
from tests.rdf_test import create_rdf_test
from normalize_naming import normalize_data
import time

start = time.time()

path_to_data = os.environ.get('DATAPATH', 'data')

print("Reading CSVs")
data = read(version='v1.7', data_root_path='data')


print("Normalizing nodes and columns")
data = normalize_data(data)

print("Creating Schema")
create_schema(data, 'schema_generated.dql')
print("Creating RDF")
create_rdf(data, 'data.rdf')
# create_rdf_test('/Users/michaelhobbs/src/csv2rdf/data.rdf')
end = time.time()
print(end - start)

