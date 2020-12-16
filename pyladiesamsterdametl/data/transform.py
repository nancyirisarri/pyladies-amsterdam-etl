"""Run R script to make output data.

"""
import csv
import os
import subprocess
from random import choice
from random import seed

import pandas as pd
import string

# seed random number generator
seed(1)


def transform():
    """Create data by running R script and do appropriate transformations.

    Returns:
        None

    """
    script = os.environ['SCRIPT']

    run_script(script)

    path_absolute_output = os.path.join(
        os.environ['RESULTS_DATA_LOCAL'],
        '{}.csv'.format(script))

    # Since not possible to determine errors in R script execution, check file.
    if not os.path.exists(path_absolute_output):
        raise Exception('R script execution error for: {}.'.format(script))

    # If making data for environment test, anonymize upn's.
    if os.environ['ENVIRONMENT'] == 'test':
        anonymize(path_absolute_output, 'Agegroup')


def run_script(script):
    """Run the R script.

    Returns:
        None

    """
    # Must change directory since R scripts use relative paths.
    os.chdir(os.path.join(os.environ['SCRIPTS_DIR'], os.environ['SOURCE']))
    # Make the file that receives subprocess stderr.
    open(os.path.join(
        os.environ['LOG_FILES_PATH'], '{}.log'.format(script)), 'w').close()

    subprocess.call(
        'Rscript --vanilla {}.R'.format(script),
        shell=True,
        stderr=open(os.path.join(
                os.environ['LOG_FILES_PATH'], '{}.log'.format(script)), 'a'),
        stdout=subprocess.DEVNULL
    )


def anonymize(path_absolute_output, column, column_length=8):
    """Anonymize a column.

    Args:
        path_absolute_output (str): Absolute path to output CSV file.
        column (str): Name of column to anonymize.
        column_length (int): Length of column values.

    Returns:
        None

    """
    df = pd.read_csv(path_absolute_output, dtype=str, na_values='')

    if column in list(df.columns):
        new_column = [
            ''.join(
                choice(string.ascii_uppercase + string.digits) for i in range(column_length))
            for j in range(df.shape[0])
        ]
        new_column = ['"{}"'.format(i) for i in new_column]

        df.drop(column, axis=1, inplace=True)

        df[column] = new_column

        df.to_csv(
            path_absolute_output,
            header=df.columns,
            index=False,
            quoting=csv.QUOTE_NONE)
