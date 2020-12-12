""" Entities """

import csv
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from os import path

months_dict = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
               'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}

days_dict = {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7}


def process_forestfires(file_path: str) -> Dict[str, List]:
    """Process a csv file of forest fire data into a dictionary
    containing a list of each column.

    Preconditions:
     - path.exists(file_path)

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
    >>> d == {'timestamp': [datetime.datetime(2000, 3, 5, 0, 0)], 'ffmc': [86.2], 'dmc': [26.2],\
              'dc': [94.3], 'isi': [5.1], 'temperature': [8.2], 'humidity': [51.0], 'wind': [6.7],\
              'rain': [0.0], 'area': [0.0]}
        True
    """
    data['timestamp'].append(datetime(2000, months_dict[row[2]], days_dict[row[3]]))
    data['ffmc'].append(float(row[4]))
    data['dmc'].append(float(row[5]))
    data['dc'].append(float(row[6]))
    data['isi'].append(float(row[7]))
    data['temperature'].append(float(row[8]))
    data['humidity'].append(float(row[9]))
    data['wind'].append(float(row[10]))
    data['rain'].append(float(row[11]))
    data['area'].append(float(row[12]))


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
        - average_temp >= -273.0
       """
    timestamp: datetime.date
    city: str
    average_temp: float
    uncertainty: float


def process_temperatures(file_path: str, city: str) -> List[PortugalTemperatureData]:
    """Process a csv file into a list of PortugalTemperatureData.

    Preconditions:
     - path.exists(file_path)
     - data at file_path is in the form as described by fileformats.txt
     - the city exists in the file

    >>> data = process_temperatures('data/portugaltemperatures.csv', 'Amadora')
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
    >>> result == PortugalTemperatureData(timestamp=datetime.datetime(1753, 1, 1, 0, 0),\
                  city='Amadora', average_temp=7.106, uncertainty=5.358)
    True
    """
    time_data = [int(x) for x in row[0].split('-')]

    return PortugalTemperatureData(timestamp=datetime(time_data[0], time_data[1],
                                   time_data[2]), city=row[3], average_temp=float(row[1]),
                                   uncertainty=float(row[2]))
