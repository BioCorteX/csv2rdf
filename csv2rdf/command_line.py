import os
import click
from csv2rdf.reader import read
from csv2rdf.schema import create_schema
from csv2rdf.rdf import create_rdf
from csv2rdf.normalize_naming import normalize_data

DATA_DIR_DEFAULT = 'data'
DATA_VERION_DEFAULT = 'demo'


@click.command()
@click.option('-d', '--data_dir', required=False, default=DATA_DIR_DEFAULT, help='Directory where to find the data')
@click.option('-v', '--data_version', required=False, default=DATA_VERION_DEFAULT,
              help='Version of the data (directory name in the data directory')
@click.option('-s', '--schema_file', required=False, default='schema_generated.dql', help='')
@click.option('-r', '--rdf_file', required=False, default='data.rdf', help='')
def main(data_dir, data_version, schema_file, rdf_file):
    if data_dir == DATA_DIR_DEFAULT:
        data_dir = os.environ.get('DATAPATH', DATA_DIR_DEFAULT)

    print("Reading CSVs")
    data = read(version=data_version, data_root_path=data_dir)

    print("Normalizing nodes and columns")
    data = normalize_data(data)

    print(f"Creating Schema: {schema_file}")
    create_schema(data, schema_file)

    print(f"Creating RDF: {rdf_file}")
    create_rdf(data, rdf_file)

    print('done')
