"""Models """

from typing import Dict, List, Tuple
import plotly.express as px
import pandas as pd
import statsmodels.api as sm
from entities import process_temperatures, process_forestfires
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
        temperatures_dc = self.trendline('temperature', 'dc', False)
        average_temps = self.get_average_temperatures()

        list_of_times = []  # ACCUMULATOR
        list_of_dc = []  # ACCUMULATOR

        for year in average_temps:
            predicted_dc = temperatures_dc[0] + temperatures_dc[1] * average_temps[year]
            list_of_times.append(year)
            list_of_dc.append(predicted_dc)
            print(year, predicted_dc)

        self.trendline_axis_known(('time', list_of_times), ('dc', list_of_dc))

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

    def trendline(self, x_axis: str, y_axis: str, display=True) -> List[float]:
        """Function to give a general trend of the input values"""
        data = process_forestfires(self.FIRES_FILE)
        df = pd.DataFrame({x_axis: data[x_axis], y_axis: data[y_axis]})
        fig = px.scatter(df, x=x_axis, y=y_axis, marginal_x="box", marginal_y="violin", trendline="ols")

        if display:
            fig.show()

        results = px.get_trendline_results(fig)
        return results.iloc[0]["px_fit_results"].params

    def trendline_axis_known(self, x_axis: Tuple[str, List[float]],
                             y_axis: Tuple[str, List[float]]) -> List[float]:
        """Function to give a general trend of the input values"""
        df = pd.DataFrame({x_axis[0]: x_axis[1], y_axis[0]: y_axis[1]})
        fig = px.scatter(df, x=x_axis[0], y=y_axis[0], marginal_x="box", marginal_y="violin", trendline="ols")
        fig.show()

        results = px.get_trendline_results(fig)
        return results.iloc[0]["px_fit_results"].params

    def animate_temperatures(self) -> None:
        """" Animation to show the increase of temperature over time.
        """
        df = pd.read_csv(self.TEMPERATURES_FILE)
        fig = px.bar(df, x="Source", y="Mean",
                     animation_frame="Year", animation_group="Source", range_y=[-1, 1])
        fig.show()

    def animate_temperatures2(self) -> None:
        """" Animation to show the increase of temperature over time.
        """
        data = self.get_average_temperatures()
        list_of_years = list(data.keys())
        list_of_temp = list(data.values())
        length = len(list_of_temp)
        list_of_city = [self.CITY] * length
        df = pd.DataFrame(dict(year=list_of_years, temp=list_of_temp,
                               city=list_of_city))
        fig = px.bar(df, x="city", y="temp",
                     animation_frame="year", animation_group="city", range_y=[0, 30])
        fig.show()


def plot_variables(indep_var1: str, indep_var2: str, dep_var: str) -> None:
    """ Plot the scatter plot of dependent variable in a 3d graph with the 2 independent variables.

    Parameters:
     - indep_var1: the name of the first independent variable for the double regression
     - indep_var2: the name of the second independent variable for the double regression
     - dep_var: the name of the dependent variable  for the double regression

    Preconditions:
     - indep_var1 in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                   'wind', 'rain', 'area']
     - indep_var2 in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                   'wind', 'rain', 'area']
     - dep_var in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                   'wind', 'rain', 'area']
    """
    # put the data from datafile into list of columns of each factor.
    data_col = process_forestfires('data/forestfires.csv')

    # generate dataframe of the columns of factors
    df = pd.DataFrame(data_col, columns=['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                                         'wind', 'rain', 'area'])

    fig = px.scatter_3d(df[[indep_var1, indep_var2, dep_var]], x=indep_var1,
                        y=indep_var2, z=dep_var, opacity=0.6)
    # generate a 3d scatter plot, the x and y axis are value of the 2 independent variables,
    # z-axis is the value for the dependent variable.
    fig.show()  # show the figure in browser


def plot_prediction_vs_outcome(dep_var: str, prediction: List[float]) -> None:
    """ Plot the prediction of a factor calculated from regression vs the actual
        values of that factor from datafile.

    Parameters:
     - dep_var: the name of the one factor that affects forestfires
                that we are looking at
     - predictions: the list of predicted value of that factor that is
                    calculated from formula of double regression

    Preconditions:
     - dep_var in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                   'wind', 'rain', 'area']
     - len(prediction) == len(process_forestfires('forestfires.csv'))
    """
    # put the data into columns of each factor.
    data_col = process_forestfires('data/forestfires.csv')

    # generate dataframe of the columns of factors
    df = pd.DataFrame(data_col, columns=['ffmc', 'dmc', 'dc', 'isi', 'temperature',
                                         'humidity', 'wind', 'rain', 'area'])

    # add the column of predictions, since it is not in data_col
    df['prediction'] = prediction

    # generate scatter plot, original value
    fig = px.scatter(df[[dep_var, 'prediction']], x=dep_var, y='prediction')

    # from the datafile on x-axis, prediction calculated from double regression on the y-axis
    fig.show()  # show the plot in browser


def calc_double_regression(y_0: float, b_1: float, b_2: float, x1: str, x2: str) -> List[float]:
    """ Calculate the value of dependent variable y using equation of double regression.

    Parameters:
        - y_0: the constant
        - b_1: the coefficient of the first variable
        - b_2: the coefficient of the second variable
        - x1: the name of the first variable
        - x2: the name of the second variable

    Preconditions:
        - x1 in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                   'wind', 'rain', 'area']
        - x2 in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                   'wind', 'rain', 'area']
        - len(process_fires_col('forestfires.csv')[x1]) == len(process_fires_col('forestfires.csv')[x2])
    """
    # get the data into dict of columns of each factor
    data_col = process_forestfires('data/forestfires.csv')
    x1_list = data_col[x1]  # get the column corresponding to x1
    x2_list = data_col[x2]  # get the column corresponding to x2
    y = []  # an empty list for the results of regression
    for i in range(len(x1_list)):  # looping through all elements in x1 and x2.
        # perform calculation of double regression using formula,
        y.append(y_0 + b_1 * x1_list[i] + b_2 * x2_list[i])
        # add the result into the list

    return y  # return the list


def model_coef_double_regression(indep_var1: str, indep_var2: str, dep_var: str) -> tuple:
    """ given 2 independent variable name and 1 dependent variable name, use statsmodel.OLS to model the
        change of dependent variable due to changes of independent variables. Returns a tuple with 3 floats,
        in the order of constant, coefficient of 1st independent variable, coefficient of 2nd independent
        variable.

    Parameters:
     - indep_var1: the name of the first independent variable
     - indep_var2: the name of the second independent variable
     - dep_var: the name of the dependent variable

    Preconditions:
     - indep_var1 in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                   'wind', 'rain', 'area']
     - indep_var2 in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                   'wind', 'rain', 'area']
     - dep_var in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                   'wind', 'rain', 'area']

    >>> model_coef_double_regression('forestfires.csv', 'ffmc', 'dc', 'temperature')
    (-14.839067312278363, 0.31592664888750815, 0.009291464340286205)
    """
    # put data into dict of columns of each factor
    data_col = process_forestfires('data/forestfires.csv')

    # generate dataframe from data_col
    df = pd.DataFrame(data_col, columns=['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                                         'wind', 'rain', 'area'])

    # x is the dataframe with only columns of the 2 independent variables
    x = df[[indep_var1, indep_var2]]

    # y is the dataframe with only column of the dependent variable
    y = df[dep_var]

    x = sm.add_constant(x)  # add a constant to x

    model = sm.OLS(y, x).fit()  # perform OSL on x and y, find the coefficients of
    # the independent variables that results in R squared closest to 1

    # get the constant and the coefficients into a dictionary
    dict_model = dict(model.params)

    # return the values of the constant, first coefficient, and second coefficient
    return (dict_model['const'], dict_model[indep_var1], dict_model[indep_var2])


# model = Model('data/forestfires.csv', 'data/portugaltemperatures.csv', 'data/annual_csv.txt', 'Braga')
