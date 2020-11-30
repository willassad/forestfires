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
        - FFMC: the Fine Fuel Moisture Code according to FWI system
        - DMC: the Duff Moisture Code according to FWI system
        - DC: the Drought Code according to FWI system
        - ISI: the Initial Spread Index according to FWI system
        - 

    Representation Invariants:
     -

    Sample Usage:
    >>>

    """
