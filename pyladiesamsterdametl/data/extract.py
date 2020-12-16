"""To download data from Storage according to R scripts.
"""
import os

import requests


def extract():
    """Read R script to determine input data and download it from Storage.

    Returns:
        None

    """
    api_endpoint = 'https://data.rivm.nl/covid-19/'
    files_raw = ['COVID-19_aantallen_gemeente_cumulatief.csv', 'COVID-19_casus_landelijk.csv']

    for file_raw in files_raw:
        file_raw_local = os.path.join(
            os.environ['RAW_DATA_LOCAL'], file_raw
        )
        r = requests.get(url='{}{}'.format(api_endpoint, file_raw))
        open(file_raw_local, 'wb').write(r.content)
