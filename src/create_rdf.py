from reader import read
from schema import create_schema
from rdf import create_rdf
from normalize_naming import normalize_data


print("Reading CSVs")
# data = read(version='demo')
data = read(version='v1.5', data_root_path='/Users/mo/Datasets/18-BioCorteX/00_POC_Final_data/')
print("Normalizing nodes and columns")
data = normalize_data(data)

print("Creating Schema")
create_schema(data, 'schema_generated.graphql')
print("Creating RDF")
create_rdf(data, 'data.rdf')

