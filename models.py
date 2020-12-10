from typing import List
import plotly.express as px
import pandas as pd
import statsmodels.api as sm
from entities import process_temperatures, process_forestfires, process_fires_col


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
        temperatures_data = process_temperatures(self.TEMPERATURES_FILE, self.CITY)

        for data_row in temperatures_data:
            temperature = data_row.average_temp
            timestamp = data_row.timestamp
            predicted_dc = temperatures_dc[0] + temperatures_dc[1] * temperature
            print(timestamp, temperature, predicted_dc)


    def predict_temperature(self, year) -> None:
        """ Predict future temperature in the given year """
        pass

    def factors_affecting_ffmc1(self) -> None:
        """ Finding out the trend of ffmc wrt temperature
        """
        list_of_data = process_forestfires(self.FIRES_FILE)
        list_of_temperature = [list_of_data[k].temperature for k in range(0, len(list_of_data))]
        list_of_ffmc = [list_of_data[k].ffmc for k in range(0, len(list_of_data))]
        df = pd.DataFrame(dict(temperature=list_of_temperature, FFMC=list_of_ffmc))
        fig = px.scatter(df, x="temperature", y="FFMC", marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

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
        fig.show()

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



def calc_double_regression(y_0: float, b_1: float, b_2: float, x1: float, x2: float) -> float:
    """ Calculate the value of dependent variable y using equaltion of double regression.

    :param y_0: constant y-intercept
    :param b_1: coefficient of first independent variable
    :param b_2: coefficient of second independent variable
    :param x1: value of the first independent variable
    :param x2: value of the second independent variable
    :return: the value of the dependent variable y.
    """
    y = y_0 + b_1 * x1 + b_2 * x2

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
