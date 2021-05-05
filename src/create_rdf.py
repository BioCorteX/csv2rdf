from reader import read
from schema import create_schema
from rdf import create_rdf
from normalize_naming import normalize_data


data = read(version='v1.2')
data = normalize_data(data)

create_schema(data, 'schema_generated.graphql')
create_rdf(data, 'data.rdf')

