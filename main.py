"""Main interactive file """
from models import Model


def main() -> None:
    """ Main function to run interactions with user. """
    model = Model('data/forestfires.csv', 'data/portugaltemperatures.csv', 'data/annual_csv.txt', 'Braga')
    print('INTERACTIVE ANALYSIS OF FOREST FIRE DATA AND CLIMATE CHANGE\n')

    print('DC is the rating of the average moisture content of deep compact organic layers.')
    print('Drought code deeply affects forest fire intensity, severity, extent, and frequency.')
    print('Let\'s first investigate the relationship between Temperature and DC.')
    model.trendline('temperature', 'dc')

    print('Average global temperatures have increased in the last couple hundred years.')
    





if __name__ == '__main__':
    main()
