from typing import Dict, List
import plotly.express as px
import pandas as pd
import statsmodels.api as sm
from entities import process_temperatures, process_forestfires, process_fires_col
import plotly.io as pio

pio.renderers.default = "browser"


class Model:
    """ Main class to model and predict forest fires. """

    def __init__(self, fires_file: str, temperatures_file: str, annual_file: str, city: str):
        # static file name paths
        self.FIRES_FILE = fires_file
        self.TEMPERATURES_FILE = temperatures_file
        self.ANNUAL_FILE = annual_file
        self.CITY = city

    def dc_versus_year(self) -> None:
        """ Look at the relationship between dc and year.
        Trying to find a trend for how the dc will change as temperatures
        change over time.

        For each year in TEMPERATURES_FILE in the city CITY, take
        the temperature and find the expected DC value from that temperature
        from the data in FIRES_FILE

        Graph the results.
        """
        temperatures_dc = self.factors_affecting_dc1()
        average_temps = self.get_average_temperatures()

        list_of_times = []  # ACCUMULATOR
        list_of_dc = []  # ACCUMULATOR

        for year in average_temps:
            predicted_dc = temperatures_dc[0] + temperatures_dc[1] * average_temps[year]
            list_of_times.append(year)
            list_of_dc.append(predicted_dc)
            print(year, predicted_dc)

        df = pd.DataFrame(dict(Time=list_of_times, DC=list_of_dc))
        fig = px.scatter(df, x="Time", y="DC", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

    def get_average_temperatures(self) -> Dict[int, float]:
        """Return a dictionary of the year corresponding to the average temperature """
        temperatures_data = process_temperatures(self.TEMPERATURES_FILE, self.CITY)
        yearly_temperatures = {}

        for row in temperatures_data:
            year = row.timestamp.year
            temperature = row.average_temp

            if year in yearly_temperatures:
                yearly_temperatures[year].append(temperature)
            else:
                yearly_temperatures[year] = []

        return {key: sum(yearly_temperatures[key]) / len(yearly_temperatures[key])
                for key in yearly_temperatures if len(yearly_temperatures[key]) > 0}

    def predict_temperature(self, year) -> None:
        """ Predict future temperature in the given year """
        temperature_data = self.get_average_temperatures()
        df = pd.DataFrame(dict(time=list(temperature_data.keys()), temperature=temperature_data.values()))
        fig = px.scatter(df, x="time", y="temperature", marginal_x="box", marginal_y="violin", trendline="ols")

        results = px.get_trendline_results(fig)
        parameters = results.iloc[0]['px_fit_results'].params
        return parameters[0] + parameters[1] * year

    def factors_affecting_ffmc1(self) -> None:
        """ Finding out the trend of ffmc wrt temperature
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_temperature = [list_of_data[k].temperature for k in range(0, len(list_of_data))]
        list_of_ffmc = [list_of_data[k].ffmc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(temperature=list_of_temperature, FFMC=list_of_ffmc))
        fig = px.scatter(df, x="temperature", y="FFMC", marginal_x="box", marginal_y="violin", trendline="ols")
        pio.show(fig)

    def factors_affecting_ffmc2(self) -> None:
        """ Finding out the trend of ffmc wrt Relative humidity
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_moisture_data = [list_of_data[k].humidity for k in range(0, len(list_of_data))]
        list_of_ffmc = [list_of_data[k].ffmc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(Relative_humidity=list_of_moisture_data,
                               FFMC=list_of_ffmc))
        fig = px.scatter(df, x="Relative_humidity", y="FFMC", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

    def factors_affecting_ffmc3(self) -> None:
        """ Finding out the trend of ffmc wrt wind speed
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_wind = [list_of_data[k].wind for k in range(0, len(list_of_data))]
        list_of_ffmc = [list_of_data[k].ffmc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(wind=list_of_wind, FFMC=list_of_ffmc))
        fig = px.scatter(df, x="wind", y="FFMC", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

    def factors_affecting_dmc1(self) -> None:
        """ Finding out the trend of dmc wrt temperature
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_temperature = [list_of_data[k].temperature for k in range(0, len(list_of_data))]
        list_of_dmc = [list_of_data[k].dmc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(temperature=list_of_temperature, DDMC=list_of_dmc))
        fig = px.scatter(df, x="temperature", y="DDMC", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

    def factors_affecting_dmc2(self) -> None:
        """ Finding out the trend of dmc wrt Relative Humidity
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_moisture_data = [list_of_data[k].humidity for k in range(0, len(list_of_data))]
        list_of_dmc = [list_of_data[k].dmc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(Relative_humidity=list_of_moisture_data, DDMC=list_of_dmc))
        fig = px.scatter(df, x="Relative_humidity", y="DDMC", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

    def factors_affecting_dmc3(self) -> None:
        """ Finding out the trend of dmc wrt wind speed
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_wind = [list_of_data[k].wind for k in range(0, len(list_of_data))]
        list_of_dmc = [list_of_data[k].dmc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(wind=list_of_wind, DDMC=list_of_dmc))
        fig = px.scatter(df, x="wind", y="DDMC", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

    def factors_affecting_dc1(self) -> List[float]:
        """ Finding out the trend of dc wrt temperature
        Return a list containing the constant, followed by coefficient of trendline
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_temperature = [list_of_data[k].temperature for k in range(0, len(list_of_data))]
        list_of_dc = [list_of_data[k].dc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(temperature=list_of_temperature, DC=list_of_dc))
        fig = px.scatter(df, x="temperature", y="DC", marginal_x="box", marginal_y="violin", trendline="ols")
        # fig.show()

        results = px.get_trendline_results(fig)
        return results.iloc[0]["px_fit_results"].params

    def factors_affecting_dc2(self) -> None:
        """ Finding out the trend of dc wrt Relative Humidity
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_moisture_data = [list_of_data[k].humidity for k in range(0, len(list_of_data))]
        list_of_dc = [list_of_data[k].dc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(Relative_humidity=list_of_moisture_data, DC=list_of_dc))
        fig = px.scatter(df, x="Relative_humidity", y="DC", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

    def factors_affecting_dc3(self) -> None:
        """ Finding out the trend of dc wrt wind speed
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_wind = [list_of_data[k].wind for k in range(0, len(list_of_data))]
        list_of_dc = [list_of_data[k].dc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(wind=list_of_wind, DC=list_of_dc))
        fig = px.scatter(df, x="wind", y="DC", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

    def factors_affecting_isi1(self) -> None:
        """ Finding out the trend of isi wrt ffmc
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_isi = [list_of_data[k].isi for k in range(0, len(list_of_data))]
        list_of_ffmc = [list_of_data[k].ffmc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(ISI=list_of_isi, FFMC=list_of_ffmc))
        fig = px.scatter(df, x="FFMC", y="ISI", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

    def factors_affecting_isi2(self) -> None:
        """ Finding out the trend of isi wrt dmc
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_isi = [list_of_data[k].isi for k in range(0, len(list_of_data))]
        list_of_dmc = [list_of_data[k].dmc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(ISI=list_of_isi, DMC=list_of_dmc))
        fig = px.scatter(df, x="DMC", y="ISI", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

    def factors_affecting_isi3(self) -> None:
        """ Finding out the trend of isi wrt dc
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_isi = [list_of_data[k].isi for k in range(0, len(list_of_data))]
        list_of_dc = [list_of_data[k].dc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(ISI=list_of_isi, DC=list_of_dc))
        fig = px.scatter(df, x="DC", y="ISI", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

    def factors_linked_temp(self) -> None:
        """ Finding out the trend of temperature wrt wind, Relative Humidity
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_moisture_data = [list_of_data[k].humidity for k in range(0, len(list_of_data))]
        list_of_temperature = [list_of_data[k].temperature for k in range(0, len(list_of_data))]
        list_of_wind = [list_of_data[k].wind for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(Relative_humidity=list_of_moisture_data,
                               wind=list_of_wind, temperature=list_of_temperature))
        fig = px.scatter(df, x="temperature", y=["wind", "Relative_humidity"], trendline="ols")
        fig.show()

    def animate_temperatures(self) -> None:
        """" Animation to show the increase of temp over time
        """
        df = pd.read_csv(self.TEMPERATURES_FILE)
        fig = px.bar(df, x="Source", y="Mean",
                     animation_frame="Year", animation_group="Source", range_y=[-1, 1])
        fig.show()


def plot_double_regression(file_name: str, indep_var1: str, indep_var2: str, dep_var: str) -> None:
    """ Plot the scatter plot of dependent variable in a 3d graph with the 2 independent variables.
    """
    data_col = process_fires_col(file_name)
    df = pd.DataFrame(data_col, columns=['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                                         'wind', 'rain', 'area'])
    fig = px.scatter_3d(df[[indep_var1, indep_var2, dep_var]], x=indep_var1, y=indep_var2, z=dep_var, opacity=0.6)
    fig.show()


def plot_prediction_vs_outcome(file_name: str, dep_var: str, prediction: List[float]) -> None:
    """ Plot the prediction calculated from regression vs the actual data from dataset
    """
    data_col = process_fires_col(file_name)
    df = pd.DataFrame(data_col, columns=['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                                         'wind', 'rain', 'area'])
    df['prediction'] = prediction
    fig = px.scatter(df[[dep_var, 'prediction']], x=dep_var, y='prediction')
    fig.show()


def calc_double_regression(file_name: str, y_0: float, b_1: float, b_2: float, x1: str, x2: str) -> List[float]:
    """ Calculate the value of dependent variable y using equaltion of double regression.
    """
    data_col = process_fires_col(file_name)
    x1_list = data_col[x1]
    x2_list = data_col[x2]
    y = []
    for i in range(len(x1_list)):
        y.append(y_0 + b_1 * x1_list[i] + b_2 * x2_list[i])

    return y


def model_coef_double_regression(file_name: str, indep_var1: str, indep_var2: str, dep_var: str) -> None:
    """ given 2 independent variable name and 1 dependent variable name, use statsmodel.OLS to model the
        change of dependent variable due to changes of independent variables.

        :param file_name: datafile we are using, the forestfire.csv file
        :param indep_var1: the first independent variable
        :param indep_var2: the second independent variable
        :param dep_var: the dependent variable
        :return: none
    """

    data_col = process_fires_col(file_name)
    df = pd.DataFrame(data_col, columns=['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                                         'wind', 'rain', 'area'])
    x = df[[indep_var1, indep_var2]]
    y = df[dep_var]
    x = sm.add_constant(x)

    model = sm.OLS(y, x).fit()
    print(model.summary())


model = Model('forestfires.csv', 'portugaltemperatures.csv', 'annual_csv.txt', 'Braga')


def main() -> None:
    """ Main """
    pass


if __name__ == '__main__':
    main()
