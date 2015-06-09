__author__ = 'kristian'

import sys

from extract_data import datatoFrame


def main(input_file):
    input_data = datatoFrame(input_file, 'dummy')
    df_filtered = input_data[input_data['honest'] == 'on']
    return df_filtered


if __name__ == '__main__':
    main(sys.argv[1])