"""forestfires Data Computations and Modelling

Overview and Description
========================

This Python module contains a class to model a location where forest fires
occur and predict how future increase in temperatures will affect these
fires. This includes methods that graph and animate the data.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2020 Will Assad, Jessica Zhai,
Raghav Banka, and Fatimeh Hassan.
"""
from typing import Dict, List, Tuple
import plotly.express as px
import plotly.io as pio
import pandas as pd
import statsmodels.api as sm
from entities import process_temperatures, process_forestfires

pio.renderers.default = 'browser'


class Model:
    """ Main class to model and predict forest fires. """
    fires_file: str
    temperatures_file: str
    city: str

    def __init__(self, fires_file: str, temperatures_file: str, city: str) -> None:
        # static file name paths
        self.fires_file = fires_file
        self.temperatures_file = temperatures_file
        self.city = city

    def plot_variables(self, indep_var1: str, indep_var2: str, dep_var: str) -> None:
        """ Plot the scatter plot of dependent variable in a 3d graph with
        the 2 independent variables.

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
        data_col = process_forestfires(self.fires_file)

        # generate dataframe of the columns of factors
        df = pd.DataFrame(data_col, columns=['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                                             'wind', 'rain', 'area'])

        fig = px.scatter_3d(df[[indep_var1, indep_var2, dep_var]], x=indep_var1,
                            y=indep_var2, z=dep_var, opacity=0.6)
        # generate a 3d scatter plot, the x and y axis are value of the 2 independent variables,
        # z-axis is the value for the dependent variable.
        fig.show()  # show the figure in browser

    def trendline(self, x_axis: str, y_axis: str,
                  show_plot: bool = True, start: int = None) -> List[float]:
        """Function to give a general trend of the input forest fire values
        starting at the x-value given by start. The default value None, means
        that the domain will not be restricted at all.

        Graph the results by default value show_plot and return linear
        regression parameters.

        Preconditions:
         - x_axis in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                      'wind', 'rain', 'area']
         - y_axis in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                      'wind', 'rain', 'area']
         - show_plot is True or show_plot is False

        >>> model = Model('data/forestfires.csv', 'data/portugaltemperatures.csv', 'Braga')
        >>> model.trendline('humidity', 'isi', False)
        [10.6615826813379, -0.03702835507934204]
        """
        # process data and get the appropriate x/y values
        data = process_forestfires(self.fires_file)
        x_axis_data = data[x_axis]
        y_axis_data = data[y_axis]

        # if the domain is restricted by start
        if start is not None:
            # get all the x-values greater than given starting point
            x_axis_data = [x for x in x_axis_data if x > start]

            # get all the corresponding y-values
            y_axis_data = [y_axis_data[i] for i in range(
                len(y_axis_data) - len(x_axis_data), len(y_axis_data))]

        # plot the values and return the linear regression parameters
        return plot_trendline_axis_known((x_axis, x_axis_data), (y_axis, y_axis_data), show_plot)

    def dc_versus_year(self) -> None:
        """ Look at the relationship between dc and year.
        Trying to find a trend for how the dc will change as temperatures
        change over time.

        For each year in TEMPERATURES_FILE in the city CITY, take
        the temperature and find the expected DC value from that temperature
        from the data in FIRES_FILE

        Graph the results in browser.
        """
        # get the results of linear regression on dc vs. temperature
        temperatures_dc = self.trendline('temperature', 'dc', False)
        average_temps = self.get_average_temperatures()

        list_of_times = []  # ACCUMULATOR: list of the years (x-axis)
        list_of_dc = []  # ACCUMULATOR: list of predicted DC (y-axis)

        # loop through each year and calculate the expected DC value
        for year in average_temps:
            # use results of linear regression to predict a dc value from temperature
            predicted_dc = temperatures_dc[0] + temperatures_dc[1] * average_temps[year]
            list_of_times.append(year)
            list_of_dc.append(predicted_dc)

        # graph the results
        plot_trendline_axis_known(('time', list_of_times), ('dc', list_of_dc))

    def plot_prediction_vs_outcome(self, dep_var: str, prediction: List[float]) -> None:
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
        data_col = process_forestfires(self.fires_file)

        # generate dataframe of the columns of factors
        df = pd.DataFrame(data_col, columns=['ffmc', 'dmc', 'dc', 'isi', 'temperature',
                                             'humidity', 'wind', 'rain', 'area'])

        # add the column of predictions, since it is not in data_col
        df['prediction'] = prediction

        # generate scatter plot, original value
        fig = px.scatter(df[[dep_var, 'prediction']], x=dep_var, y='prediction')

        # from the datafile on x-axis, prediction calculated from double regression on the y-axis
        fig.show()  # show the plot in browser

    def predict_temperature(self, year: int) -> float:
        """ Predict future temperature in the given year in self.CITY

        Preconditions:
         - year >= min(self.get_average_temperatures().keys())

         >>> model = Model('data/forestfires.csv', 'data/portugaltemperatures.csv', 'Amadora')
         >>> model.predict_temperature(2060)
         16.670193437009456
        """
        # get parameters of linear regression and return predicted temperature
        temperature_data = self.get_average_temperatures()
        parameters = plot_trendline_axis_known(('Year', list(temperature_data.keys())),
                                               ('Temperature', list(temperature_data.values())),
                                               False)
        return parameters[0] + parameters[1] * year

    def animate_temperatures(self) -> None:
        """" Function to plot the average temperature of a particular city
        for each year in an animated bar chart.
        """
        # process data from datafile and get a dictionary datatype
        data = self.get_average_temperatures()
        # get a list of keys and values from the dictionary
        list_of_years = list(data.keys())
        list_of_temp = list(data.values())
        length = len(list_of_temp)
        list_of_city = [self.city] * length
        # generate dataframe from the list of keys and values from the dictionary
        df = pd.DataFrame(dict(year=list_of_years, temp=list_of_temp,
                               city=list_of_city))
        # plot animated bar chart taking the average temperatures as the y axis,
        # city to be the x axis and the frame of reference to be the years concerned
        fig = px.bar(df, x="city", y="temp",
                     animation_frame="year", animation_group="city", range_y=[0, 30])
        # to display the bar chart
        fig.show()

    def get_average_temperatures(self) -> Dict[int, float]:
        """Return a dictionary of the year corresponding to the average temperature """
        temperatures_data = process_temperatures(self.temperatures_file, self.city)
        yearly_temperatures = {}  # ACCUMULATOR: map each year to a list of all the
        # temperatures recorded in that year

        for row in temperatures_data:
            year = row.timestamp.year
            temperature = row.average_temp

            # mutate list or create it if it does not exist
            if year in yearly_temperatures:
                yearly_temperatures[year].append(temperature)
            else:
                yearly_temperatures[year] = []

        # return the average of all the temperatures of each year
        return {key: sum(yearly_temperatures[key]) / len(yearly_temperatures[key])
                for key in yearly_temperatures if len(yearly_temperatures[key]) > 0}

    def calc_double_regression(self, params: Tuple[float, float, float],
                               x1: str, x2: str) -> List[float]:
        """ Calculate the value of dependent variable y using equation of double regression.

        Parameters:
            - params: the constant, coefficient of the first variable
                and the coefficient of the second variable
            - x1: the name of the first independent variable
            - x2: the name of the second independent variable

        Preconditions:
            - x1 in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                       'wind', 'rain', 'area']
            - x2 in ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity',
                       'wind', 'rain', 'area']
            - len(process_fires_col('forestfires.csv')[x1]) ==
              len(process_fires_col('forestfires.csv')[x2])

        >>> model = Model('data/forestfires.csv', 'data/portugaltemperatures.csv', 'Amadora')
        >>> result = model.calc_double_regression((2, 3, 4), 'ffmc', 'dmc')
        >>> result[1] == 415.4
        True
        """
        # get the data into dict of columns of each factor
        data_col = process_forestfires(self.fires_file)

        x1_list = data_col[x1]  # get the column corresponding to x1
        x2_list = data_col[x2]  # get the column corresponding to x2
        y = []  # ACCUMULATOR: the results of regression

        for i, val in enumerate(x1_list):  # looping through all elements in x1 and x2.
            # perform calculation of double regression using formula,
            y.append(params[0] + params[1] * val + params[2] * x2_list[i])
            # add the result into the list

        return y  # return the list

    def coef_double_regression(self, indep_var1: str, indep_var2: str, dep_var: str) -> tuple:
        """ given 2 independent variable names and 1 dependent variable name, use
            statsmodel.OLS to model the change of dependent variable due to changes
            of independent variables. Returns a tuple with 3 floats, in the order of constant,
            coefficient of 1st independent variable, coefficient of 2nd independent
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

        >>> m = Model('data/forestfires.csv', 'data/portugaltemperatures.csv', 'Braga')
        >>> m.coef_double_regression('ffmc', 'dc', 'temperature')
        (-14.839067312278363, 0.31592664888750815, 0.009291464340286205)
        """
        # put data into dict of columns of each factor
        data_col = process_forestfires(self.fires_file)

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


def plot_trendline_axis_known(x_axis: Tuple[str, List[float]], y_axis: Tuple[str, List[float]],
                              show_plot: bool = True) -> List[float]:
    """Function to give a general trend of the input values

    >>> x_axis_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    >>> y_axis_data = [2.0, 4.0, 6.0, 8.0, 10.0]
    >>> plot_trendline_axis_known(('x-axis', x_axis_data), ('y-axis', y_axis_data), False)
    [-3.1086244689504383e-15, 2.0000000000000004]
    """
    df = pd.DataFrame({x_axis[0]: x_axis[1], y_axis[0]: y_axis[1]})
    fig = px.scatter(df, x=x_axis[0], y=y_axis[0], marginal_x="box",
                     marginal_y="violin", trendline="ols")

    if show_plot:  # default is to display plot
        fig.show()

    # get results of linear regression and return
    results = px.get_trendline_results(fig)
    return list(results.iloc[0]["px_fit_results"].params)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['python_ta.contracts', 'typing', 'plotly.express',
                          'pandas', 'statsmodels.api', 'entities', 'plotly.io'],
        'allowed-io': ['process_forestfires', 'process_temperatures']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()
