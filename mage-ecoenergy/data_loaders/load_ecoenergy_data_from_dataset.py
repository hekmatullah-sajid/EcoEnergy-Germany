from mage_ai.io.file import FileIO
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import requests
import os
import pandas as pd

@data_loader
def load_ecoenergy_data_from_dataset(*args, **kwargs):
    """
    This data loader will check if data already exist, 
    if not it will downlaod the dataset into data dir
    and then read the data
    """
    # dataset_url = "https://data.open-power-system-data.org/renewable_power_plants/2020-08-25/renewable_power_plants_DE.csv"

    dataset_url =  os.environ.get('DATASET_URL')
    # Extracting filename of the dataset from URL
    filename = dataset_url.split("/")[-1]

    # Path to the file in the data directory
    filepath = os.path.join("data", filename)

    # If the file already exists, then no needed to download it
    # If the file not exists, then download it
    if os.path.exists(filepath):
        print("Dataset already downloaded and exists.")
    else:
        print("Downloading the dataset.")
        response = requests.get(dataset_url)

        if response.status_code == 200:
            print("Dataset downloaded successfully!")
            print("Processing the dataset.")

            # Chekc if the data directory exists, if not create it
            if not os.path.exists("data"):
                os.makedirs("data")
            
            # Writing content to the file in the data directory
            with open(filepath, "wb") as f:
                f.write(response.content)
        else:
            print("Failed to download the dataset:", response.status_code)
    
    # maping dataset data types 
    ecoenergy_dtypes = {
        'electrical_capacity': float,
        'energy_source_level_1': str,
        'energy_source_level_2': str,
        'energy_source_level_3': str,
        'technology': str,
        'data_source': str,
        'nuts_1_region': str,
        'nuts_2_region': str,
        'nuts_3_region': str,
        'lon': float,
        'lat': float,
        'municipality': str,
        'municipality_code': str,
        'postcode': str,
        'address': str,
        'federal_state': str,
        #'commissioning_date': object,
        #'decommissioning_date': object,
        'voltage_level': str,
        'eeg_id': str,
        'dso': str,
        'dso_id': str,
        'tso': str
    }
    # Date columns 
    parse_dates = ['commissioning_date', 'decommissioning_date']
    
    # date parser function as native date parser return datetime, the cols are date only
    def custom_date_parser(date_string):
        return pd.to_datetime(date_string).date()

    ecoenergy_df = pd.read_csv(filepath, sep=',', dtype=ecoenergy_dtypes, parse_dates=parse_dates)
    
    # the next date conversion is for BigQuery, without this the date is stored as datetime
    ecoenergy_df['commissioning_date'] = ecoenergy_df['commissioning_date'].dt.date
    ecoenergy_df['decommissioning_date'] = ecoenergy_df['decommissioning_date'].dt.date

    print("Processing the dataset completed.")

    return ecoenergy_df



@test
def test_data_ingestion_output(output, *args) -> None:
    """
    Testing the output of the data ingestion block to ensure that 
    the dataset was successfully downloaded and its content was read.
    """
    assert output is not None, 'The output of the data ingestion block is empty.'
