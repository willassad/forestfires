# Import dataset
from dataclasses import dataclass
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
    >>> oct_fire = ForestFireData(month=10, day=6, ffmc=90.6,dmc=43.7, dc=686.9,\
                                  isi=6.7, temperature=14.6, humidity=33, wind=1.3,\
                                  rain=0, area=0)
    """

    month: int
    day: int
    ffmc: float
    dmc: float
    dc: float
    isi: float
    temperature: float
    humidity: float
    wind: float
    rain: float
    area: float


def process_csv(file: str) -> List[ForestFireData]:
    """Process a csv file into a list of ForestFireData"""
    pass


def row_to_forest_data(row: str) -> ForestFireData:
    """ Convert a row of forestfires.csv into ForestFireData

    >>> sample_row = '7,4,oct,tue,90.6,35.4,669.1,6.7,18,33,0.9,0,0'
    >>> row_to_forest_data(sample_row)
    ForestFireData(month=10, day=2, ffmc=90.6, dmc=35.4, dc=669.1,
                   isi=6.7, temperature=18.0, humidity=33.0,
                   wind=0.9, rain=0.0, area=0.0)
    """
    lst = row.split(',')
    month = months_dict[lst[2]]
    day = days_dict[lst[3]]

    return ForestFireData(month=month, day=day, ffmc=float(lst[4]), dmc=float(lst[5]),
                          dc=float(lst[6]), isi=float(lst[7]), temperature=float(lst[8]),
                          humidity=float(lst[9]), wind=float(lst[10]),
                          rain=float(lst[11]), area=float(lst[12]))
