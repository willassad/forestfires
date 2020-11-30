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
        - relative_humidity: the humidity of the area where fire started
        - wind: the amount of wind in the area where the fire started
        - rain: the amount of rain in the area where the fire started
        - area: the area of forest burned

    Representation Invariants:
     - 0 <= self.month <= 12
     - 0 <= self.day <= 31
     - 0.0 <= self.ffmc <= 101.0
     - 

    Sample Usage:
    >>>

    """
