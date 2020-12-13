"""Main interactive file """
from models import Model


def main() -> None:
    """ Main function to run interactions with user. """
    model = Model('data/forestfires.csv', 'data/portugaltemperatures.csv', 'Braga')
    print('INTERACTIVE ANALYSIS OF FOREST FIRE DATA AND CLIMATE CHANGE')
    print('Location: Montesinho National Park, Portugal')

    print('\nAverage regional temperatures have increased in the last couple hundred years.')
    input('Press any key to open animation >>> ')
    model.animate_temperatures()

    print('\nDC is the rating of the average moisture content of deep compact organic layers.')
    print('Drought code deeply affects forest fire intensity, severity, extent, and frequency.')
    print('Let\'s first investigate the relationship between Temperature and DC.')
    input('Press any key to open graph >>> ')
    model.trendline('temperature', 'dc')

    print('\nWhile temperature increase has been gradual in Portugal, we can predict that the')
    print('DC will also increase over time as temperatures increase.')
    input('Press any key to open graph >>> ')
    model.dc_versus_year()

    print('\nWe might expect a fire in conditions with low humidity and high temperature to spread quicker.')
    print('ISI is a measure of how quickly a forest fire spreads.')
    print('Let\'s do a double regression plotting these variables.')
    input('Press any key to continue >>> ')

    result = model.coef_double_regression('temperature', 'humidity', 'isi')
    print('\nLet t be temperature. Let h be humidity. Let I be a function that maps temperature and humidity')
    print('to the expected ISI value. We get the following trend:')
    print(f'I(t, h) = {result[1]}t + {result[2]}h + {result[0]}')
    input('\nPress any key to open graph >>> ')
    model.plot_variables('temperature', 'humidity', 'isi')

    print('\nWould you like to examine any other variables? Press \'y\'. Otherwise, press any other key.')
    to_continue = input()
    while to_continue.upper() == 'Y':
        print('Pick two of the following variables: ')

        print('\nWould you like to examine any other variables? Press \'y\'. Otherwise, press any other key.')
        to_continue = input()


if __name__ == '__main__':
    main()
