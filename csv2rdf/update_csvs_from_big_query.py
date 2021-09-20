import os
from datetime import datetime, timedelta
from typing import List
import pandas as pd
import pytz
from google.cloud import bigquery
"""
Must set google authentification in environment variables. 
See here: https://cloud.google.com/docs/authentication/getting-started#cloud-console
e.g.
export GOOGLE_APPLICATION_CREDENTIALS = '/some/path/to/json_credentials/example.json'

In pycharm these can be added to the run configuration by going to the dropdown next to the run button in the top right,
and clicking edit configurations. Then in environment variables add the key value pair
"""
BQ_PROJECT = os.environ.get('BQ_PROJECT', 'biocortex')
BQ_DATASET = os.environ.get('BQ_DATASET', 'Bo_v1_7')
BQ_UPDATE_ALL_TABLES = os.environ.get('BQ_UPDATE_ALL_TABLES', False)
BQ_UPDATE_INTERVAL = os.environ.get('BQ_UPDATE_INTERVAL', 90000)  # 1 day, 1 hour - In future can check for presence of local file and compare modification dates

BQ_DATASET_ID = BQ_PROJECT + '.' + BQ_DATASET
BQ_CLIENT = bigquery.Client()
LOCALIZE_TIME = pytz.UTC


def list_table_ids():
    result = BQ_CLIENT.list_tables(BQ_DATASET_ID)
    table_ids = [table.table_id for table in result]
    return table_ids


def list_table_ids_with_changes(update_interval: int) -> List[str]:
    """
    get table that have been updated in the time interval given
    :param update_interval: how long ago (in seconds) to check for changes to tables
    :return: List of table_ids as strings
    """
    update_delta = LOCALIZE_TIME.localize(datetime.now() - timedelta(seconds=int(update_interval)))
    result = BQ_CLIENT.list_tables(BQ_DATASET_ID)
    if BQ_UPDATE_ALL_TABLES:
        table_ids = [table.table_id for table in result]
    else:
        tables = [BQ_CLIENT.get_table(table.reference) for table in result]
        table_ids = [table.table_id for table in tables if table.modified > update_delta]
    return table_ids


def get_dataframe_from_tableid(table_id) -> pd.DataFrame:
    query_string = f"""
    SELECT * 
    FROM `{BQ_DATASET_ID}.{table_id}`
    """
    dataframe = (
        BQ_CLIENT.query(query_string)
        .result()
        .to_dataframe(
        )
    )
    return dataframe


def update_csvs():
    out_of_date_table_ids = list_table_ids_with_changes(update_interval=BQ_UPDATE_INTERVAL)
    data_dir_path = os.path.join('data', BQ_DATASET)
    os.makedirs(data_dir_path, exist_ok=True)
    for table_id in out_of_date_table_ids:
        df = get_dataframe_from_tableid(table_id)
        csv_path = os.path.join(data_dir_path, table_id + '.csv')
        df.to_csv(csv_path, index=False)
        print(str(datetime.now()) + "\t" + f'BigQuery table \'{table_id}\' downloaded')


if __name__ == '__main__':
    update_csvs()
