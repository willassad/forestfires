"""forestfires Reading Data

Overview and Description
========================

This Python module contains the data class definitions and functions to read
datasets located in the data subdirectory. In some cases, data is read as
dictionaries with the key as the column name and values as a list of values.
In other cases, we use Python's dataclass to represent a row of temperature
data.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2020 Will Assad, Jessica Zhai,
Raghav Banka, and Fatimeh Hassan.
"""
import csv
from dataclasses import dataclass
import datetime
from typing import List, Dict

# this import statement is used in preconditions, but PythonTA and PyCharm cannot detect this.
import os

MONTHS_DICT = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
               'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}

DAYS_DICT = {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7}


@dataclass
class PortugalTemperatureData:
    """We represent a row of temperature data in portugal by storing
       the timestamp, city, the average temperature in that city during
       that time, and the uncertainty.

       Attributes:
        - timestamp: the time when the temperature was recorded
        - city: the city where the temperature was recorded
        - average_temp: the average temperature recorded
        - uncertainty: the uncertainty of the measurement

       Representation Invariants:
        - self.average_temp >= -273.0
       """
    timestamp: datetime.datetime
    city: str
    average_temp: float
    uncertainty: float


def process_temperatures(file_path: str, city: str) -> List[PortugalTemperatureData]:
    """Process a csv file into a list of PortugalTemperatureData.

    Preconditions:
     - os.path.exists(file_path)
     - data at file_path is in the form as described by fileformats.md
     - the city exists in the file

    >>> data = process_temperatures('data/portugaltemperatures2.csv', 'Amadora')
    >>> data[0].average_temp == 7.106
    True
    """
    with open(file_path) as file:
        reader = csv.reader(file)

        data_so_far = []  # ACCUMULATOR: update list of data
        for row in reader:
            if city in row and row[1] != '':
                # process each row and add to data_so_far
                data_so_far.append(row_to_temperature_data(row))

    return data_so_far


def row_to_temperature_data(row: List[str]) -> PortugalTemperatureData:
    """ Convert a row of forestfires.csv into PortugalTemperatureData

    >>> example_row = ['1753-01-01', '7.106', '5.358', 'Amadora', 'Portugal', '39.38N', '8.32W']
    >>> result = row_to_temperature_data(example_row)
    >>> result.uncertainty == 5.358
    True
    """
    time_data = [int(x) for x in row[0].split('-')]

    return PortugalTemperatureData(timestamp=datetime.datetime(time_data[0], time_data[1],
                                                               time_data[2]), city=row[3],
                                   average_temp=float(row[1]), uncertainty=float(row[2]))


def process_forestfires(file_path: str) -> Dict[str, List]:
    """Process a csv file of forest fire data into a dictionary
    containing a list of each column.

    Preconditions:
     - os.path.exists(file_path)

    >>> data = process_forestfires('data/forestfires.csv')
    >>> data['temperature'][0] == 8.2
    True
    """
    with open(file_path) as file:
        reader = csv.reader(file)
        next(reader)  # skip header

        data_so_far = {'timestamp': [], 'ffmc': [], 'dmc': [], 'dc': [], 'isi': [],
                       'temperature': [], 'humidity': [], 'wind': [],
                       'rain': [], 'area': []}  # ACCUMULATOR: update dict of data
        for row in reader:
            # process each row and add to data_so_far
            add_row_to_dict(data_so_far, row)

    return data_so_far


def add_row_to_dict(data: Dict[str, List], row: List[str]) -> None:
    """Mutate dictionary data_so_far to add row

    >>> d = {'timestamp': [], 'ffmc': [], 'dmc': [], 'dc': [], 'isi': [],\
            'temperature': [], 'humidity': [], 'wind': [],\
            'rain': [], 'area': []}
    >>> r = ['7', '5', 'mar', 'fri', '86.2', '26.2', '94.3', '5.1', '8.2', '51', '6.7', '0', '0']
    >>> add_row_to_dict(d, r)
    >>> d['ffmc'] == [86.2]
    True
    """
    data['timestamp'].append(datetime.datetime(2000, MONTHS_DICT[row[2]], DAYS_DICT[row[3]]))
    data['ffmc'].append(float(row[4]))
    data['dmc'].append(float(row[5]))
    data['dc'].append(float(row[6]))
    data['isi'].append(float(row[7]))
    data['temperature'].append(float(row[8]))
    data['humidity'].append(float(row[9]))
    data['wind'].append(float(row[10]))
    data['rain'].append(float(row[11]))
    data['area'].append(float(row[12]))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['python_ta.contracts', 'dataclasses', 'datetime', 'os', 'typing', 'csv'],
        'allowed-io': ['process_forestfires', 'process_temperatures'],
        'disable': ['W0611']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()
