from reader import read
from schema import create_schema
from rdf import create_rdf
from normalize_naming import normalize_data


print("Reading CSVs")
data = read(version='v1.4', data_root_path='data')
print("Normalizing nodes and columns")
data = normalize_data(data)

print("Creating Schema")
create_schema(data, 'schema_generated.dql')
print("Creating RDF")
create_rdf(data, 'data.rdf')

