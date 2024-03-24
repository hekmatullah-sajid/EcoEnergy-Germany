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
    Template for exporting data to a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery
    """

    project_id = os.environ.get('GCP_PROJECT_ID') # GCS Peoject ID
    dataset_id = os.environ.get('BIGQUERY_DATASET') # GCS BigQuery Dataset
    table_id = "ecoenergy_data"

    table_id = f'{project_id}.{dataset_id}.{table_id}'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    
    # df['commissioning_date']=df['commissioning_date'].dt.date
    # df['decommissioning_date']=df['decommissioning_date'].dt.date
    
    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        table_id,
        if_exists='replace',  # Replace if table name already exists
    )
