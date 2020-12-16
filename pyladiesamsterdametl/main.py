"""Determine input data from R script, extract it from Storage, run R script to
make output data, and make table in BigQuery.

"""
import logging
import os
import sys

from .data.extract import extract
from .data.load import load
from .data.transform import transform
from .logs.logs import delete_previous_log_files
from .logs.logs import upload_log_file

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


def main():
    """Run each of the steps.

    Returns:
        None

    """
    scripts = os.environ[
        os.environ['SCRIPTS'].format(os.environ['SOURCE'].upper())
    ].split()

    for script in scripts:
        try:
            os.environ['SCRIPT'] = script

            extract()

            transform()

            load()

        except Exception as e:
            logger.setLevel(logging.CRITICAL)
            logger.critical('Error in script: {}.'.format(script))
            logger.critical(e, exc_info=True)

            try:
                upload_log_file(script)

            except:
                logger.setLevel(logging.ERROR)
                logger.error('Error in upload_log_file.')

            continue


def takeoff():
    """Run each of the steps.

    Returns:
        None

    """
    delete_previous_log_files()

    main()


if __name__ == "__main__":
    for c in os.environ['SOURCES'].split():
        os.environ['SOURCE'] = c
        try:
            takeoff()
        except Exception as e:
            logger.setLevel(logging.CRITICAL)
            logger.critical(e, exc_info=True)
