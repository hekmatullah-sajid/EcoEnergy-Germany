from pandas import DataFrame
import pyarrow as pa
import pyarrow.parquet as pq
import os
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


# JSON user key for authentication with GCP
gcp_credentials =  os.environ.get('GCP_CREDENTIALS')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"/home/src/secrets/{gcp_credentials}"

bucket_name = os.environ.get('GCS_BUCKET') # GCS bucket name
folder_name = 'ecoenergy_data' # Folder name inside bucket where your data will be stored

root_path = f'{bucket_name}/{folder_name}'
file_name_csv = os.environ.get('DATASET_URL').split("/")[-1]
file_name_parquet = file_name_csv.replace(".csv", ".parquet")
@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    
    # Exporting ecoenergy data to a Google Cloud Storage bucket.
    pyarrow_table = pa.Table.from_pandas(df)

    gcs_uri = f'gs://{root_path}/{file_name_parquet}'
    pq.write_table(pyarrow_table, gcs_uri)

    print("Parquet file was successfully written to GCS bucket")
"""
@test
def test_write_file_to_gcs(*args) -> None:
        # Replace 'your_table' with your actual PyArrow table
        
        # Create example data to test writing to GCS
        data = {
            'electrical_capacity': [1.5, 0.25, 0.93],
            'energy_source_level_1': ['Renewable energy', 'Renewable energy', 'Renewable energy'],
            'energy_source_level_2': ['Hydro', 'Wind', 'Solar']
        }

        # Create PyArrow table from example data
        table = pa.Table.from_pandas(pd.DataFrame(data))


        test_table = table
        gcs_uri = f'gs://{root_path}/test.parquet'

        test_result = pq.write_table(test_table, gcs_uri)

        # Assert that write_table was called with the expected filename
        assert test_result is not False, 'Falied writing file to GCS.'
"""