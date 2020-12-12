"""Main interactive file """
from models import Model, model_coef_double_regression


def main() -> None:
    """ Main function to run interactions with user. """
    model = Model('data/forestfires.csv', 'data/portugaltemperatures.csv', 'data/annual_csv.txt', 'Braga')
    print('INTERACTIVE ANALYSIS OF FOREST FIRE DATA AND CLIMATE CHANGE')
    print('Location: Montesinho National Park, Portugal')

    print('\nAverage regional temperatures have increased in the last couple hundred years.')
    input('Press any key to open animation >>> ')
    #model.animate_temperatures2()

    print('\nDC is the rating of the average moisture content of deep compact organic layers.')
    print('Drought code deeply affects forest fire intensity, severity, extent, and frequency.')
    print('Let\'s first investigate the relationship between Temperature and DC.')
    input('Press any key to open graph >>> ')
    #model.trendline('temperature', 'dc')

    print('\nWhile temperature increase has been gradual in Portugal, we can predict that the')
    print('DC will also increase over time as temperatures increase.')
    input('Press any key to open graph >>> ')
    #model.dc_versus_year()

    print('\nWe might expect a fire in conditions with low humidity and high temperature to spread quicker.')
    print('ISI is a measure of how quickly a forest fire spreads.')
    print('Let\'s do a double regression plotting these variables.')
    input('Press any key to continue >>> ')
    result = model_coef_double_regression('temperature', 'humidity', 'isi')





if __name__ == '__main__':
    main()
