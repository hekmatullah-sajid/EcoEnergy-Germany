from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:
    """
    Block for exporting renewable energy data to BigQuery data-warehouse.
    """
    
    print("Exporting renewable energy data to BigQuery ...")

    # Set GOOGLE_APPLICATION_CREDENTIALS for authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ.get('GCP_CREDENTIALS')

    project_id = os.environ.get('GCP_PROJECT_ID') # GCP Peoject ID
    dataset_id = os.environ.get('BIGQUERY_DATASET') # BigQuery Dataset
    table_name = os.environ.get('BIGQUERY_TABLE') # table name to create inside BigQuery
    table_id = f'{project_id}.{dataset_id}.{table_name}'


    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
        
    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        table_id,
        if_exists='replace',  # Replace if table name already exists
    )
