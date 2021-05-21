import os
import click
from reader import read
from schema import create_schema
from rdf import create_rdf
from normalize_naming import normalize_data

data_dir_default = 'data'
data_version_default = 'demo'


@click.command()
@click.option('-d', '--data_dir', required=False, default=data_dir_default, help='Directory where to find the data')
@click.option('-v', '--data_version', required=False, default=data_version_default, help='Version of the data (directory name in the data directory')
@click.option('-s', '--schema_file', required=False, default='schema_generated.dql', help='')
@click.option('-r', '--rdf_file', required=False, default='data.rdf', help='')
def main(data_dir, data_version, schema_file, rdf_file):
    if data_dir == data_dir_default:
      data_dir = os.environ.get('DATAPATH', data_dir_default)

    print("Reading CSVs")
    data = read(version=data_version, data_root_path=data_dir)

    print("Normalizing nodes and columns")
    data = normalize_data(data)

    print(f"Creating Schema: {schema_file}")
    create_schema(data, schema_file)

    print(f"Creating RDF: {rdf_file}")
    create_rdf(data, rdf_file)

    print('done')
