"""Manipulate R script error log files.

"""
import os

import glob
from google.cloud import storage


def delete_previous_log_files():
    """Delete from bucket earlier files and from container previous client-year.

    Returns:
        None

    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
        os.environ['LOG_FILES_PROJECT_GCP_KEY']

    client = storage.Client(project=os.environ['LOG_FILES_PROJECT_GCP'])

    cloud_bucket = client.lookup_bucket(
        os.environ['LOG_FILES_BUCKET'].format(os.environ['SOURCE']))
    if cloud_bucket is not None:
        blobs = cloud_bucket.list_blobs()
        for blob in blobs:
            cloud_bucket.blob(blob.name).delete()

    # Delete logs from the container from previous client-year.
    log_files = glob.glob('{}/*.log'.format(os.environ['LOG_FILES_PATH']))
    for f in log_files:
        os.remove(f)


def upload_log_file(script):
    """Upload log file created in transform.run_script.

    Args:
        script (str): Name of the script.

    Returns:
        None

    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
        os.environ['LOG_FILES_PROJECT_GCP_KEY']
    client = storage.Client(project=os.environ['LOG_FILES_PROJECT_GCP'])

    bucket_name = os.environ['LOG_FILES_BUCKET'].format(os.environ['SOURCE'])

    # Look up the bucket and if None then create it.
    cloud_bucket = client.lookup_bucket(bucket_name)
    if cloud_bucket is None:
        client.create_bucket(bucket_name)
        cloud_bucket = client.get_bucket(bucket_name)

    file_name = '{}.log'.format(script)

    blob = cloud_bucket.blob(file_name)
    blob.upload_from_filename(filename=os.path.join(
        os.environ['LOG_FILES_PATH'], file_name))
