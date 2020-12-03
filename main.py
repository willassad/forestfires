# import dataset
import csv
from dataclasses import dataclass
from datetime import datetime
from typing import List
import plotly.express as px
import pandas as pd


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
            if city in row:
                # process each row and add to data_so_far
                data_so_far.append(row_to_temperature_data(row))

    return data_so_far


def row_to_temperature_data(row: List[str]) -> PortugalTemperatureData:
    """ Convert a row of forestfires.csv into PortugalTemperatureData
    """
    time_data = [int(x) for x in row[0].split('-')]

    return PortugalTemperatureData(timestamp=datetime(time_data[0], time_data[1],
                                   time_data[2]), city=row[3], average_temp=float(row[1]),
                                   uncertainty=float(row[2]))


def factors_affecting_ffmc1(file_name: str) -> None:
    """ Finding out the trend of ffmc wrt temperature
    """
    list_of_data = process_forestfires(file_name)
    list_of_temperature = [list_of_data[k].temperature for k in range(0, len(list_of_data))]
    list_of_ffmc = [list_of_data[k].ffmc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(temperature=list_of_temperature, FFMC=list_of_ffmc))
    fig = px.scatter(df, x="temperature", y="FFMC", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_affecting_ffmc2(file_name: str) -> None:
    """ Finding out the trend of ffmc wrt Relative humidity
    """
    list_of_data = process_forestfires(file_name)
    list_of_moisture_data = [list_of_data[k].humidity for k in range(0, len(list_of_data))]
    list_of_ffmc = [list_of_data[k].ffmc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(Relative_humidity=list_of_moisture_data,
                           FFMC=list_of_ffmc))
    fig = px.scatter(df, x="Relative_humidity", y="FFMC", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_affecting_ffmc3(file_name: str) -> None:
    """ Finding out the trend of ffmc wrt wind speed
    """
    list_of_data = process_forestfires(file_name)
    list_of_wind = [list_of_data[k].wind for k in range(0, len(list_of_data))]
    list_of_ffmc = [list_of_data[k].ffmc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(wind=list_of_wind,  FFMC=list_of_ffmc))
    fig = px.scatter(df, x="wind", y="FFMC", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_affecting_dmc1(file_name: str) -> None:
    """ Finding out the trend of dmc wrt temperature
    """
    list_of_data = process_forestfires(file_name)
    list_of_temperature = [list_of_data[k].temperature for k in range(0, len(list_of_data))]
    list_of_dmc = [list_of_data[k].dmc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(temperature=list_of_temperature, DDMC=list_of_dmc))
    fig = px.scatter(df, x="temperature", y="DDMC", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_affecting_dmc2(file_name: str) -> None:
    """ Finding out the trend of dmc wrt Relative Humidity
    """
    list_of_data = process_forestfires(file_name)
    list_of_moisture_data = [list_of_data[k].humidity for k in range(0, len(list_of_data))]
    list_of_dmc = [list_of_data[k].dmc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(Relative_humidity=list_of_moisture_data, DDMC=list_of_dmc))
    fig = px.scatter(df, x="Relative_humidity", y="DDMC", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_affecting_dmc3(file_name: str) -> None:
    """ Finding out the trend of dmc wrt wind speed
    """
    list_of_data = process_forestfires(file_name)
    list_of_wind = [list_of_data[k].wind for k in range(0, len(list_of_data))]
    list_of_dmc = [list_of_data[k].dmc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(wind=list_of_wind, DDMC=list_of_dmc))
    fig = px.scatter(df, x="wind", y="DDMC", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_affecting_dc1(file_name: str) -> None:
    """ Finding out the trend of dc wrt temperature
    """
    list_of_data = process_forestfires(file_name)
    list_of_temperature = [list_of_data[k].temperature for k in range(0, len(list_of_data))]
    list_of_dc = [list_of_data[k].dc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(temperature=list_of_temperature, DC=list_of_dc))
    fig = px.scatter(df, x="temperature", y="DC", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_affecting_dc2(file_name: str) -> None:
    """ Finding out the trend of dc wrt Relative Humidity
    """
    list_of_data = process_forestfires(file_name)
    list_of_moisture_data = [list_of_data[k].humidity for k in range(0, len(list_of_data))]
    list_of_dc = [list_of_data[k].dc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(Relative_humidity=list_of_moisture_data, DC=list_of_dc))
    fig = px.scatter(df, x="Relative_humidity", y="DC", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_affecting_dc3(file_name: str) -> None:
    """ Finding out the trend of dc wrt wind speed
    """
    list_of_data = process_forestfires(file_name)
    list_of_wind = [list_of_data[k].wind for k in range(0, len(list_of_data))]
    list_of_dc = [list_of_data[k].dc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(wind=list_of_wind,  DC=list_of_dc))
    fig = px.scatter(df, x="wind", y="DC", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_affecting_isi1(file_name: str) -> None:
    """ Finding out the trend of isi wrt ffmc
    """
    list_of_data = process_forestfires(file_name)
    list_of_isi = [list_of_data[k].isi for k in range(0, len(list_of_data))]
    list_of_ffmc = [list_of_data[k].ffmc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(ISI=list_of_isi, FFMC=list_of_ffmc))
    fig = px.scatter(df, x="FFMC", y="ISI", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_affecting_isi2(file_name: str) -> None:
    """ Finding out the trend of isi wrt dmc
    """
    list_of_data = process_forestfires(file_name)
    list_of_isi = [list_of_data[k].isi for k in range(0, len(list_of_data))]
    list_of_dmc = [list_of_data[k].dmc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(ISI=list_of_isi, DMC=list_of_dmc))
    fig = px.scatter(df, x="DMC", y="ISI", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_affecting_isi3(file_name: str) -> None:
    """ Finding out the trend of isi wrt dc
    """
    list_of_data = process_forestfires(file_name)
    list_of_isi = [list_of_data[k].isi for k in range(0, len(list_of_data))]
    list_of_dc = [list_of_data[k].dc for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(ISI=list_of_isi, DC=list_of_dc))
    fig = px.scatter(df, x="DC", y="ISI", marginal_x="box", marginal_y="violin", trendline="ols")
    fig.show()


def factors_linked_temp(file_name: str) -> None:
    """ Finding out the trend of temperature wrt wind, Relative Humidity
    """
    list_of_data = process_forestfires(file_name)
    list_of_moisture_data = [list_of_data[k].humidity for k in range(0, len(list_of_data))]
    list_of_temperature = [list_of_data[k].temperature for k in range(0, len(list_of_data))]
    list_of_wind = [list_of_data[k].wind for k in range(0, len(list_of_data))]
    df = pd.DataFrame(dict(Relative_humidity=list_of_moisture_data,
                           wind=list_of_wind, temperature=list_of_temperature))
    fig = px.scatter(df, x="temperature", y=["wind", "Relative_humidity"], trendline="ols")
    fig.show()


def main() -> None:
    """ Main """
    pass
