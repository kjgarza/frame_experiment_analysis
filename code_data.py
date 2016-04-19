__author__ = 'kristian'

import sys
import math
import pandas as pd
import datetime

from extract_data import datatoFrame


def main(input_file):

    input_data = datatoFrame(input_file, 'dummy')
    # print input_data


def code_baseline(series):

    # codes =pd.DataFrame.from_csv('helpers/baseline_codes.csv')

    # cat_series = series.merge(codes, on='when_best', how='left')
    # series['baseline'] = pd.Series(0, index=series.index)
    # series['baseline'] = cat_series

    series['baseline'] = pd.Series(0, index=series.index)
    series.baseline[series['when_best'] == '+10 years after publication of a peer-review paper'] = 1
    series.baseline[series['when_best'] == '+5 years after publication of a peer-review paper'] = 2
    series.baseline[series['when_best'] == '+3 years after publication of a peer-review paper'] = 3
    series.baseline[series['when_best'] == '+1 years after publication of a peer-review paper'] = 4
    series.baseline[series['when_best'] == 'immediately after publication of a peer-review paper'] = 5
    series.baseline[series['when_best'] == 'before publication of a peer-review paper'] = 6

    return series


def code_control(series):

    codes =pd.DataFrame.from_csv('helpers/control_codes.csv')

    cat_series = series.merge(codes, on='with_who', how='left')

    return cat_series


def code_treatment(series):

    series['measure'] = pd.Series(0, index=series.index)
    series.measure[series['with_who_2'] != 'public'] = 1
    series.measure[series['with_who_2'] == 'public'] = 5
    series.measure[series['when_to_2'] == '3'] = 3
    series.measure[series['when_to_2'] == '1'] = 4
    series.measure[series['when_to_2'] == '1'] = 4

    return series

def code_measures(series):

    df_filtered = series
    df_filtered['measure_2'] = pd.Series(0, index=df_filtered.index)
    df_filtered['measure_1'] = pd.Series(0, index=df_filtered.index)
    d = df_filtered[df_filtered['treatment'] == 'CONTROL']


    d.measure_1[d['with_who_1'] == 'public'] = 5
    d.measure_1[d['with_who_1'] == 'collaborators'] = 1
    d.measure_1[d['with_who_1'] == 'private'] = 1

    d.measure_2[d['with_who_2'] != 'public'] = 1
    d.measure_2[d['with_who_2'] == 'public'] = 5
    d.measure_2[d['when_to_2'] == '10'] = 2
    d.measure_2[d['when_to_2'] == '3'] = 3
    d.measure_2[d['when_to_2'] == '6'] = 4
    d.measure_2[d['when_to_2'] == '1'] = 4


    df = df_filtered[df_filtered['treatment'] == 'TREATMENT']

    df.measure_2[df['with_who_2'] == 'public'] = 5
    df.measure_2[df['with_who_2'] == 'collaborators'] = 1
    df.measure_2[df['with_who_2'] == 'private'] = 1

    df.measure_1[df['with_who_1'] != 'public'] = 1
    df.measure_1[df['with_who_1'] == 'public'] = 5
    df.measure_1[df['when_to_1'] == '10'] = 2
    df.measure_1[df['when_to_1'] == '3'] = 3
    df.measure_1[df['when_to_1'] == '6'] = 4
    df.measure_1[df['when_to_1'] == '1'] = 4

    r = df.append(d)

    return r


def code_measures_wo_scc(series):

    df_filtered = series
    df_filtered['measure_2'] = pd.Series(0, index=df_filtered.index)
    df_filtered['measure_1'] = pd.Series(0, index=df_filtered.index)
    d = df_filtered[df_filtered['treatment'] == 'CONTROL']


    d.measure_1[d['with_who_1'] == 'public'] = 5
    d.measure_1[d['with_who_1'] == 'collaborators'] = 3
    d.measure_1[d['with_who_1'] == 'private'] = 1

    # d.measure_2[d['with_who_2'] != 'public'] = 1
    d.measure_2[d['with_who_2'] == 'public'] = 5
    d.measure_2[d['with_who_2'] == 'collaborators'] = 3
    d.measure_2[d['with_who_2'] == 'private'] = 1
    # d.measure_2[d['when_to_2'] == '10'] = 2
    # d.measure_2[d['when_to_2'] == '3'] = 3
    # d.measure_2[d['when_to_2'] == '6'] = 4
    # d.measure_2[d['when_to_2'] == '1'] = 4


    df = df_filtered[df_filtered['treatment'] == 'TREATMENT']

    df.measure_2[df['with_who_2'] == 'public'] = 5
    df.measure_2[df['with_who_2'] == 'collaborators'] = 3
    df.measure_2[df['with_who_2'] == 'private'] = 1

    # df.measure_1[df['with_who_1'] != 'public'] = 1
    df.measure_1[df['with_who_1'] == 'public'] = 5
    df.measure_1[df['with_who_2'] == 'collaborators'] = 3
    df.measure_1[df['with_who_2'] == 'private'] = 1
    # df.measure_1[df['when_to_1'] == '10'] = 2
    # df.measure_1[df['when_to_1'] == '3'] = 3
    # df.measure_1[df['when_to_1'] == '6'] = 4
    # df.measure_1[df['when_to_1'] == '1'] = 4

    r = df.append(d)

    return r

def code_measures_wo_scc2(series):

    df_filtered = series
    df_filtered['measure_2'] = pd.Series(0, index=df_filtered.index)
    df_filtered['measure_1'] = pd.Series(0, index=df_filtered.index)
    d = df_filtered[df_filtered['treatment_eval_1'] == 'Jam Share Data']


    d.measure_1[d['with_who_1'] == 'public'] = 5
    d.measure_1[d['with_who_1'] == 'collaborators'] = 3
    d.measure_1[d['with_who_1'] == 'private'] = 1

    # d.measure_2[d['with_who_2'] != 'public'] = 1
    d.measure_2[d['with_who_2'] == 'public'] = 5
    d.measure_2[d['with_who_2'] == 'collaborators'] = 3
    d.measure_2[d['with_who_2'] == 'private'] = 1
    # d.measure_2[d['when_to_2'] == '10'] = 2
    # d.measure_2[d['when_to_2'] == '3'] = 3
    # d.measure_2[d['when_to_2'] == '6'] = 4
    # d.measure_2[d['when_to_2'] == '1'] = 4


    df = df_filtered[df_filtered['treatment_eval_1'] == 'cite DataLabour']

    df.measure_2[df['with_who_2'] == 'public'] = 5
    df.measure_2[df['with_who_2'] == 'collaborators'] = 3
    df.measure_2[df['with_who_2'] == 'private'] = 1

    # df.measure_1[df['with_who_1'] != 'public'] = 1
    df.measure_1[df['with_who_1'] == 'public'] = 5
    df.measure_1[df['with_who_1'] == 'collaborators'] = 3
    df.measure_1[df['with_who_1'] == 'private'] = 1
    # df.measure_1[df['when_to_1'] == '10'] = 2
    # df.measure_1[df['when_to_1'] == '3'] = 3
    # df.measure_1[df['when_to_1'] == '6'] = 4
    # df.measure_1[df['when_to_1'] == '1'] = 4

    r = df.append(d)

    return r



def code_measures_new(series):
    #Create the columns measures at give it's value via the coding scheme


    df_filtered = series
    df_filtered['measure_2'] = pd.Series(0, index=df_filtered.index)
    df_filtered['measure_1'] = pd.Series(0, index=df_filtered.index)
    dx = df_filtered[df_filtered['treatment_eval_1'] == 'Jam Share Data']

    for index, row in df_filtered.iterrows():
        if row['treatment_eval_1'] == 'Jam Share Data':
            if row['with_who_1'] == 'public':
                    df_filtered.measure_1 = 5
            if row['with_who_1'] == 'collaborators':
                    dx.measure_1 = 1
            if row['with_who_1'] == 'stakeholders':
                    df_filtered.measure_1 = 1
            if row['with_who_1'] == 'private':
                    df_filtered.measure_1 = 1
        elif row['treatment_eval_1'] == 'cite DataLabour':
            if row['with_who_1'] == 'public':
                    df_filtered.measure_1 = 5
            if row['with_who_1'] == 'collaborators':
                    df_filtered.measure_1 = 3
            if row['with_who_1'] == 'stakeholders':
                    df_filtered.measure_1 = 4
            if row['with_who_1'] == 'private':
                    df_filtered.measure_1 = 1
        if row['treatment_eval_2'] == 'Jam Share Data':
            if row['with_who_2'] == 'public':
                    df_filtered.measure_1 = 5
            if row['with_who_2'] == 'collaborators':
                    dx.measure_1 = 1
            if row['with_who_2'] == 'stakeholders':
                    df_filtered.measure_1 = 1
            if row['with_who_2'] == 'private':
                    df_filtered.measure_1 = 1
        elif row['treatment_eval_2'] == 'cite DataLabour':
            if row['with_who_2'] == 'public':
                    df_filtered.measure_1 = 5
            if row['with_who_2'] == 'collaborators':
                    df_filtered.measure_1 = 3
            if row['with_who_2'] == 'stakeholders':
                    df_filtered.measure_1 = 4
            if row['with_who_2'] == 'private':
                    df_filtered.measure_1 = 1
    return df_filtered

def code_when_to(series):
    #Create the columns measures at give it's value via the coding scheme


    r = ""

    return r


def code_usability_num_cat(w):
    r = w
    if w == 1:
        r = 'Strongly Disagree'
    elif w == 2:
        r = 'Disagree'
    elif w == 3:
        r = 'Neither'
    elif w == 4:
        r = 'Agree'
    elif w == 5:
        r = 'Strongly Agree'
    return r

def code_when_to_num_cat(t, w):
    from datetime import date
    r = w
    if t == 'Jam Share Data':
        if w == 'later':
            r = '10y'
        elif w != 'null' and type(w) is not float:
            # print (type(w))
            # release = datetime.datetime.strptime(w, "%d/%m/%Y").date()
            release = datetime.datetime.strptime(w, "%m/%Y").date()
            # print release
            today = date.today()
            grace_period = abs(release - today)
            if grace_period.days <= 400 and grace_period.days >= 180:
                r = '1y'
            elif grace_period.days >= 400 and grace_period.days <= 1400:
                r = '3y'
            elif grace_period.days >= 1401 and grace_period.days <= 3650:
                r = '10y'
            elif grace_period.days > 3651:
                r = '10y+'
            elif grace_period.days >= 0 and grace_period.days <= 179:
                r = '6m'

    # if t == 'cite DataLabour' and w == True and w != 'null' and math.isnan(w) == False:
    #     w = str(int(w))
    #     print w
    #     if w == '1':
    #         r = '1y'
    #     elif w == '6':
    #         r = '6m'
    #     elif w == '3':
    #         r = '3y'
    #     elif w == '10':
    #         r = '10y'
    # elif t == 'Jam Share Data':
    #     if w == 'later':
    #         r = '10y'
    # print r
    return r

def batch_code(df_filtered):

    df_filtered['support_1'] = df_filtered.apply(lambda row: code_usability_num_cat(row['support_1']), axis=1)
    df_filtered['support_2'] = df_filtered.apply(lambda row: code_usability_num_cat(row['support_2']), axis=1)
    df_filtered['ease_1'] = df_filtered.apply(lambda row: code_usability_num_cat(row['ease_1']), axis=1)
    df_filtered['ease_2'] = df_filtered.apply(lambda row: code_usability_num_cat(row['ease_2']), axis=1)
    df_filtered['time_1'] = df_filtered.apply(lambda row: code_usability_num_cat(row['time_1']), axis=1)
    df_filtered['time_2'] = df_filtered.apply(lambda row: code_usability_num_cat(row['time_2']), axis=1)
    df_filtered['regret_1'] = df_filtered.apply(lambda row: code_usability_num_cat(row['regret_1']), axis=1)
    df_filtered['regret_2'] = df_filtered.apply(lambda row: code_usability_num_cat(row['regret_2']), axis=1)

    df_filtered['when_to_1'] = df_filtered.apply(lambda row: code_when_to_num_cat(row['treatment_eval_1'],row['when_to_1']), axis=1)
    df_filtered['when_to_2'] = df_filtered.apply(lambda row: code_when_to_num_cat(row['treatment_eval_2'],row['when_to_2']), axis=1)
    return df_filtered




def code_openess_numeric(t,w):
    r = ""
    if t == 'Jam Share Data':
        if w == 'public':
                r = 4
        elif w == 'collaborators':
                r = 2
        elif w == 'stakeholders':
                r = 3
        elif w == 'private':
                r = 1
    elif t == 'cite DataLabour':
        if w == 'public':
                r = 4
        elif w == 'collaborators':
                r = 2
        elif w == 'stakeholders':
                r = 3
        elif w == 'private':
                r = 1
    r = r
    return r


def code_openess_labels(t,w):
    r = ""
    if t == 'Jam Share Data':
        if w == 'public':
                r = 5
        elif w == 'collaborators':
                r = 1
        elif w == 'stakeholders':
                r = 1
        elif w == 'private':
                r = 1
    elif t == 'cite DataLabour':
        if w == 'public':
                r = 5
        elif w == 'collaborators':
                r = 3
        elif w == 'stakeholders':
                r = 4
        elif w == 'private':
                r = 1
    r = w
    return r


def code_treatment_numeric(t):
    r = ""
    if t == 'Jam Share Data':
         r =0
    elif t == 'cite DataLabour':
         r = 1
    return r






if __name__ == '__main__':
    # main(sys.argv[1])
    # code_when_to_num_cat('Jam Share Data', '02/28/2015')
    code_when_to_num_cat('Jam Share Data', '08/2018')