# Import dataset
from dataclasses import dataclass


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
                                  isi=6.7, temperature=14.6, humiditiy=33, wind=1.3,\
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
