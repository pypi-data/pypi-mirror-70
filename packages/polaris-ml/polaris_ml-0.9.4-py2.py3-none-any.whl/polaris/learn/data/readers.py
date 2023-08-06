"""
Helpers to incorporate data from different sources.

General input standard format for functions in polaris learn are Pandas
Dataframe.
"""

import json
import logging
import os

import pandas as pd

LOGGER = logging.getLogger(__name__)


class PolarisUnknownFileFormatError(Exception):
    """Raised when we don't know how to read the file format
    """


def read_polaris_data(path, csv_sep=','):
    """Read a JSON or CSV file and creates a pandas dataframe out of it.

    :param path: File path for the input file.
    :param csv_sep: The csv separator used for the input csv file.
    :return: Pandas dataframe with all frames fields values and
    the data source name.
    """
    source = None
    dataframe = None

    if path.lower().endswith('.csv'):
        source, dataframe = read_polaris_data_from_csv(path, csv_sep)

    elif path.lower().endswith('.json'):
        source, dataframe = read_polaris_data_from_json(path)

    else:
        LOGGER.critical("Don't know how to load from file %s ", path)
        raise PolarisUnknownFileFormatError

    return source, dataframe


def read_polaris_data_from_csv(path, csv_sep=','):
    """Read Polaris data from CSV

    :param path: File path for the input file.
    :param csv_sep: The csv separator used for the input csv file.
    :return: Pandas dataframe with all frames fields values and
    the data source name.
    """
    try:
        dataframe = pd.read_csv(path, sep=csv_sep)
        dataframe = normalize_dataframe(dataframe)
        source = os.path.splitext(path)[0]
        return source, dataframe

    except FileNotFoundError as exception_error:
        LOGGER.critical(exception_error)
        raise exception_error


def read_polaris_data_from_json(path):
    """Read Polaris data from JSON

    :param path: File path for the input file.
    :return: Pandas dataframe with all frames fields values and
    the data source name.
    """
    try:
        with open(path, "r") as json_file:
            json_data = json.load(json_file)
    except Exception as exception_error:
        LOGGER.critical(exception_error)
        raise exception_error

    source = json_data["metadata"]["satellite_name"]
    json_records = records_from_satnogs_frames(json_data)
    # Creating a pandas dataframe
    dataframe = pd.DataFrame(json_records)
    dataframe = normalize_dataframe(dataframe)
    return source, dataframe


def records_from_satnogs_frames(json_data):
    """
        Records that can be read as following format by pandas:
        '[{"col 1":"a","col 2":"b"},{"col 1":"c","col 2":"d"}]'

        :param json_data: polaris fetch format for normalized frames
    """

    records = []

    for frame in json_data["frames"]:
        # reset current record (row)
        this_record = {}

        # scan all fields
        for field in frame["fields"]:
            this_record[field] = frame["fields"][field]["value"]

        # check if we had the time information from frame
        # if not we use the metadata
        if "time" not in this_record:
            this_record["time"] = pd.to_datetime(frame["time"]).timestamp()

        records.append(this_record)

    return records


def normalize_dataframe(dataframe):
    """
        Apply dataframe modification for being used
        by the learn module.

        :param dataframe: the pandas dataframe to normalize
        :return: Pandas dataframe normalized
    """
    dataframe.index = dataframe.time
    dataframe.drop(['time'], axis=1, inplace=True)

    # Keep numeric values only
    dataframe = dataframe.select_dtypes(include=['number', 'datetime'])

    return dataframe
