from pandas import DataFrame
import pyarrow as pa
import pyarrow.parquet as pq
import os
import pandas as pd



if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

bucket_name = os.environ.get('GCS_BUCKET') # GCS bucket name
folder_name = 'ecoenergy_data' # Folder name inside bucket where your data will be stored

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ.get('GCP_CREDENTIALS')

root_path = f'{bucket_name}/{folder_name}'
file_name_csv = os.environ.get('DATASET_URL').split("/")[-1]
file_name_parquet = file_name_csv.replace(".csv", ".parquet")
@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    
    # Exporting ecoenergy data to a Google Cloud Storage bucket.
    print("Creating pyarrow table.")
    pyarrow_table = pa.Table.from_pandas(df)
    print("Writing parquet file to GCS.")
    gcs_uri = f'gs://{root_path}/{file_name_parquet}'
    pq.write_table(pyarrow_table, gcs_uri)

    print("Parquet file was successfully written to GCS Bucket.")