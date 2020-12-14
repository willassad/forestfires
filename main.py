"""forestfires Main Interactive File

Overview and Description
========================

This Python file is the main interactive file of our program where a user
can interact with our data and perform computations. This is a simple
console implementation using plotly.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2020 Will Assad, Jessica Zhai,
Raghav Banka, and Fatimeh Hassan.
"""
from models import Model, plot_trendline_axis_known


def main() -> None:
    """ Main function to run interactions with user. """

    model = Model('data/forestfires.csv', 'data/portugaltemperatures.csv', 'Braga')
    print('INTERACTIVE ANALYSIS OF FOREST FIRE DATA AND CLIMATE CHANGE')
    print('Location: Montesinho National Park, Portugal')

    print('\nAverage regional temperatures have increased in the last couple hundred years.')
    input('Press any key to open animation >>> ')
    model.animate_temperatures()

    print('\nWe can also see a graph here. Press any key to open graph >>> ')
    result = model.get_average_temperatures()
    plot_trendline_axis_known(('time', list(result.keys())), ('temperature', list(result.values())))

    print('\nDC is the rating of the average moisture content of deep compact organic layers.')
    print('Drought code deeply affects forest fire intensity, severity, extent, and frequency.')
    print('Let\'s first investigate the relationship between Temperature and DC.')
    input('Press any key to open graph >>> ')
    model.trendline('temperature', 'dc')

    print('\nWhile temperature increase has been gradual in Portugal, we can predict that the')
    print('DC will also increase over time as temperatures increase.')
    input('Press any key to open graph >>> ')
    model.dc_versus_year()

    print('\nWe might expect a fire in conditions with low humidity '
          'and high temperature to spread quicker.')
    print('ISI is a measure of how quickly a forest fire spreads.')
    print('Let\'s do a double regression plotting these variables.')
    input('Press any key to continue >>> ')

    result = model.coef_double_regression('temperature', 'humidity', 'isi')
    print('\nLet t be temperature. Let h be humidity. Let I be a function that '
          'maps temperature and humidity')
    print('to the expected ISI value. We get the following trend:')
    print(f'I(t, h) = {result[1]}t + {result[2]}h + {result[0]}')
    input('\nPress any key to open graph >>> ')
    model.plot_variables('temperature', 'humidity', 'isi')

    to_continue = input('\nWould you like to examine any other variables? Press \'y\'. '
                        'Otherwise, press any other key>>> ')

    # let user continue to examine other variables until other key is pressed
    while to_continue.upper() == 'Y':
        variables = ['ffmc', 'dmc', 'dc', 'isi', 'temperature', 'humidity', 'wind', 'rain', 'area']
        print('\nPick two of the following variables: ')
        print(', '.join([f'\'{v}\'' for v in variables]))
        variable_1 = input('\nDependent Variable >>> ')
        variable_2 = input('Independent Variable >>> ')

        # loop until valid variables are selected as input
        while variable_1 not in variables or variable_2 not in variables:
            print('[INVALID INPUT] variable not in possible variables')
            variable_1 = input('Dependent Variable >>> ')
            variable_2 = input('Independent Variable >>> ')

        input('\nPress any key to show graph >>> ')
        model.trendline(variable_2, variable_1)

        print('\nWould you like to examine any other variables? Press \'y\'. '
              'Otherwise, press any other key.')
        to_continue = input()

    print('\nHave a nice day!')


if __name__ == '__main__':
    main()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['models', 'python_ta.contracts'],
        'allowed-io': ['main']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()
