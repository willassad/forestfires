# Import dataset
import csv
from dataclasses import dataclass
from datetime import datetime
from typing import List

months_dict = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
               'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}

days_dict = {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7}


@dataclass
class ForestFireData:
    """We describe a forest fire in the same format as forestfires.csv
       where each forest fire has a month, day, FFMC, DMC, DC, ISI,
       temperature, RH, wind, rain, and area.

    Attributes:
        - month: the month when the fire occurred
        - day: the day of the month the fire occurred
        - ffmc: the Fine Fuel Moisture Code according to FWI system
        - dmc: the Duff Moisture Code according to FWI system
        - dc: the Drought Code according to FWI system
        - isi: the Initial Spread Index according to FWI system
        - temperature: the temperature of the area where the fire started
        - humidity: the relative humidity of the area where fire started
        - wind: the amount of wind in the area where the fire started
        - rain: the amount of rain in the area where the fire started
        - area: the area of forest burned

    Representation Invariants:
     - 0 <= self.month <= 12
     - 1 <= self.day <= 7
     - 0.0 <= self.ffmc <= 101.0
     - 0.0 <= self.dmc
     - 0.0 <= self.dc <= 1000.0
     - 0.0 <= self.isi
     - self.temperature.isdigit()
     - self.humidity.isdigit()
     - 0.0 <= self.wind
     - 0.0 <= self.rain
     - 0.0 <= self.area

    Sample Usage:
    >>> oct_fire = ForestFireData(timestamp=datetime(2003, 10, 2), ffmc=90.6,dmc=43.7, dc=686.9,\
                                  isi=6.7, temperature=14.6, humidity=33, wind=1.3,\
                                  rain=0, area=0)
    """

    timestamp: datetime.date
    ffmc: float
    dmc: float
    dc: float
    isi: float
    temperature: float
    humidity: float
    wind: float
    rain: float
    area: float


def process_forestfires(file_path: str) -> List[ForestFireData]:
    """Process a csv file into a list of ForestFireData"""
    with open(file_path) as file:
        reader = csv.reader(file)

        # skip header
        next(reader)

        data_so_far = []  # ACCUMULATOR: update list of data
        for row in reader:
            # process each row and add to data_so_far
            data_so_far.append(row_to_forest_data(row))

    return data_so_far


def row_to_forest_data(row: List[str]) -> ForestFireData:
    """ Convert a row of forestfires.csv into ForestFireData

    >>> sample_row = ['7','4','oct','tue','90.6','35.4','669.1','6.7','18','33','0.9','0','0']
    >>> row_to_forest_data(sample_row)
    ForestFireData(month=10, day=2, ffmc=90.6, dmc=35.4, dc=669.1,
                   isi=6.7, temperature=18.0, humidity=33.0,
                   wind=0.9, rain=0.0, area=0.0)
    """
    month = months_dict[row[2]]
    day = days_dict[row[3]]

    return ForestFireData(timestamp=datetime(2000, month, day), ffmc=float(row[4]), dmc=float(row[5]),
                          dc=float(row[6]), isi=float(row[7]), temperature=float(row[8]),
                          humidity=float(row[9]), wind=float(row[10]),
                          rain=float(row[11]), area=float(row[12]))


@dataclass
class PortugalTemperatureData:
    """Docstring """
    timestamp: datetime.date
    city: str
    average_temp: float
    uncertainty: float


def process_temperatures(file_path: str, city: str) -> List[PortugalTemperatureData]:
    """Process a csv file into a list of PortugalTemperatureData"""
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
    """
    time_data = [int(x) for x in row[0].split('-')]
    print(row)

    return PortugalTemperatureData(timestamp=datetime(time_data[0], time_data[1],
                                   time_data[2]), city=row[3], average_temp=float(row[1]),
                                   uncertainty=float(row[2]))


def main() -> None:
    """ Main """
    pass
