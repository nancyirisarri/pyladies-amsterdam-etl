"""Load data to a BigQuery table or external table.

"""
import os

from google.api_core.exceptions import BadRequest
from google.cloud import bigquery


def load_table(client, table_id):
    """Load local CSV file to an external BigQuery table.

    Args:
        client (google.cloud.bigquery.client.Client): BigQuery client object.
        table_id (str): Desired table id in BigQuery.

    Returns:
        None

    """
    path_absolute_output = os.path.join(os.environ['RESULTS_DATA_LOCAL'], '{}.csv'.format(os.environ['SCRIPT']))

    # Set the LoadJobConfig for creating the table.
    job_config = bigquery.LoadJobConfig()
    job_config.skip_leading_rows = 1
    job_config.create_disposition = 'CREATE_IF_NEEDED'

    # Define the schema.
    with open(path_absolute_output) as f:
        headers = f.readline().replace('"', '').replace('\n', '').split(',')
    schema = []
    for i in headers:
        if i in ['province']:
            schema.append(bigquery.SchemaField(i, 'STRING'))
        elif i == 'ts_load':
            schema.append(bigquery.SchemaField(i, 'TIMESTAMP'))
        else:
            schema.append(bigquery.SchemaField(i, 'INTEGER'))
    job_config.schema = schema

    # Load the table.
    load_job = client.load_table_from_file(
        open(path_absolute_output, 'rb'),
        table_id,
        job_config=job_config
    )

    # Waits for table load to complete and raises errors, like BadRequest if
    # file in combination with schema has errors.
    result_load_job = load_job.result()
    if result_load_job is not None and result_load_job.error_result is not None:
        raise Exception('Load job result errors: {}.'.format(
                result_load_job.error_result))


def backup_table(client, table_ref_source, table_ref_destination):
    """Copy source table to backup destination table, then delete source table.

    Args:
        client (google.cloud.bigquery.client.Client): BigQuery client object.
        table_ref_source (google.cloud.bigquery.table.TableReference): Source table.
        table_ref_destination (google.cloud.bigquery.table.TableReference): Destination table.

    Returns:
        None

    """
    client.delete_table(table_ref_destination, not_found_ok=True)

    job = client.copy_table(
        table_ref_source,
        table_ref_destination,
        location="EU",
    )
    result_copy_job = job.result()
    if result_copy_job is not None and result_copy_job.error_result is not None:
        raise Exception('Copy job result errors: {}.'.format(
            result_copy_job.error_result))

    client.delete_table(table_ref_source, not_found_ok=True)


def prepare_load(client, dataset_source_id, table_name):
    """Create BigQuery dataset if necessary and backup existing tables.

    Args:
        client (google.cloud.bigquery.client.Client): BigQuery client object.
        dataset_source_id (str): Source dataset id.
        table_name (str): Table name.

    Returns:
        None

    """
    dataset_source = bigquery.Dataset(dataset_source_id)
    dataset_source.location = 'EU'
    client.create_dataset(dataset_source, exists_ok=True)

    # If table exists, copy to dataset with name that has _backup appended.
    if table_name in [
            i.table_id for i in client.list_tables(dataset_source_id)]:
        dataset_destination = bigquery.Dataset(
            '{}_backup'.format(dataset_source_id))

        # Create backup
        # datasets = list(client.list_datasets())

        dataset_destination.location = 'EU'
        client.create_dataset(dataset_destination, exists_ok=True)

        backup_table(
            client,
            dataset_source.table(table_name),
            dataset_destination.table(table_name))


def rollback_table(client, table_name, dataset_id):
    """Copy a backup table to a destination table.

    Args:
        client (google.cloud.bigquery.client.Client): BigQuery client object.
        table_name (str): Table name.
        dataset_id (str): Destination dataset id.

    Returns:
        None

    """
    dataset_backup_id = '{}_backup'.format(dataset_id)
    dataset_backup = bigquery.Dataset(dataset_backup_id)
    dataset_destination = bigquery.Dataset(dataset_id)
    client.create_dataset(dataset_destination, exists_ok=True)
    if table_name in [
        i.table_id for i in client.list_tables(dataset_backup_id)]:
        job = client.copy_table(
            dataset_backup.table(table_name),
            dataset_destination.table(table_name),
            location="EU",
        )
        result_copy_job = job.result()
        if result_copy_job is not None and result_copy_job.error_result is not None:
            raise Exception('Rollback job result errors: {}.'.format(
                result_copy_job.error_result))
    else:
        raise Exception('Rollback found no backup table.')


def load():
    """Load the ouput data CSV files to BigQuery.

    Returns:
        None

    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ[
        'GOOGLE_CLOUD_PROJECT_KEY']
    gcp_project = os.environ['GOOGLE_CLOUD_PROJECT']
    # TODO Can we set the location here?
    client = bigquery.Client(project=gcp_project)
    dataset_id = '{}.{}'.format(gcp_project,
                                os.environ[
                                    os.environ['DATASET_BIG_QUERY']
                                    .format(os.environ['SOURCE'].upper())])
    table_id = '{}.{}'.format(
        dataset_id, os.environ['SCRIPT'].replace('-', '_'))
    table_name = '{}'.format(os.environ['SCRIPT'].replace('-', '_'))

    prepare_load(client, dataset_id, table_name)

    try:
        load_table(client, table_id)
    except BadRequest:
        rollback_table(client, table_name, dataset_id)
