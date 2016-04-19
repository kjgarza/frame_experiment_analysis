__author__ = 'kristian'
from extract_data import datatoFrame
from code_data import *
import numpy as np
import pandas as pd
import datetime
from datetime import date
import helpers.GibberishDetector.gib_detect_train as gb_train
import helpers.GibberishDetector.gib_detect as gb
from scipy.stats import mode
import random
import re


class FrameExperimentTable:

    def __init__(self, data):
        new_data = datatoFrame(data, 'dummy4', 'new')
        # new_data['scenario'] = '1'
        self.data = new_data
        # new_data = pd.DataFrame.from_csv('logs/data_scramble_filled_csv.csv', sep=',', index_col=0)
        # pieces = [self.data, new_data]
        # self.data = pd.concat(pieces)
        self.data = self.data.replace(['stackeholders'],['stakeholders'])

        self.data["index"] = self.data.index
        self.data.drop_duplicates(cols='index', take_last=True, inplace=True)
        del self.data["index"]


        self.data_for_analy = pd.DataFrame()
        self.data_for_plots = pd.DataFrame()
        print self.data.shape

    def add_records(self, source, method):
        """
        adds sources to the main data object
        :param source: csv file
        """
        #define method either new or old
        assert type(source) is basestring
        new_data = datatoFrame(source, 'dummy4', method)
        pieces = [self.data, new_data]
        self.data = pd.concat(pieces)
        self.data = self.data.replace(['stackeholders'],['stakeholders'])

        # self.data["index"] = self.data.index
        # self.data.drop_duplicates(cols='index', take_last=True, inplace=True)
        # del self.data["index"]
        # self.data = self.data.drop_duplicates()


    def add_records_w_scenario(self, source, scenario):
        """
        adds sources to the main data object
        :param source: csv file
        """
        #define method either new or old
        assert type(source) is basestring
        new_data = datatoFrame(source, 'dummy4', 'new')
        new_data['scenario'] = scenario
        pieces = [self.data, new_data]
        self.data = pd.concat(pieces)
        self.data = self.data.replace(['stackeholders'],['stakeholders'])


    def add_records_csv(self, source):
        """
        adds sources to the main data object
        :param source: csv file
        """
        #define method either new or old
        assert type(source) is basestring
        new_data = pd.DataFrame.from_csv(source, sep=',', index_col=0)
        # new_data = pd.DataFrame.from_csv('logs/data_scramble_filled_csv.csv', sep=',', index_col=0)
        pieces = [self.data, new_data]
        self.data = pd.concat(pieces)
        self.data = self.data.replace(['stackeholders'],['stakeholders'])


    def get_data(self):

        return self.data.copy(deep=True)

    def get_plotdata(self):

        return self.data_for_plots.copy(deep=True)

    def get_anadata(self):

        return self.data_for_analy.copy(deep=True)


    def detect_gibberish(self):
        """
        returns a filtered data object

        :return:
        """
        data = self.data.copy(deep=True)
        data['gibberish'] = data.apply(lambda row: gb.detect(str(row['discipline'])+" "+str(row['materials_type'])), axis=1)
        self.data = data

    def classify_field(self):
        """
        returns a filtered data object

        :return:
        """

        import difflib

        fields_vocab = pd.DataFrame.from_csv('logs/disciplines_list',header=0)

        data = self.data.copy(deep=True)

        def add_field(row, fields_vocab):
            r =''
            d = difflib.get_close_matches(row,fields_vocab,1)
            # print d[0]
            if d:
                r = d[0]
                # r = 'LS'
            return r

        data['field'] = data.apply(lambda row: add_field(str(row['discipline']),fields_vocab['field']), axis=1)

        print 'classify_field - Fields Excluded'
        print data.discipline[data['field'] == ''].shape
        # print data.discipline[data['field'] == '']

        self.data = data





    def filter_noise(self):
        """
        returns a filtered data object

        :return:
        """
        self.detect_gibberish()
        self.classify_field()
        self.compute_usability_metric()
        self.code_tongue()
        self.code_ways()
        # self.code_awareness()

        data_filtered = self.data.copy(deep=True)


        print "Total"
        total = data_filtered.shape[0]
        full = data_filtered
        # print total
        data_filtered =  full[(full['gibberish'] == True)]
        ## filter gibberish
        print "Removing testing"
        testing = data_filtered.shape[0]
        # print total-testing

        total = data_filtered.shape[0]
        data_filtered =  data_filtered[(data_filtered['academic'] < 3)]
        ## filter gibberish
        print "Removing Random"
        randoms = data_filtered.shape[0]
        # print total-randoms

        total = data_filtered.shape[0]
        data_filtered =  data_filtered[(data_filtered['field'] != '')]
        ## filter gibberish
        print "Removing Not Life Sciences"
        not_life = data_filtered.shape[0]
        # print total-not_life

        total = data_filtered.shape[0]
        data_filtered =  data_filtered[(data_filtered['tongue'] == 'skilled')]
        ## filter gibberish
        print "Removing Not enlgish skilled"
        englished = data_filtered.shape[0]
        # print total-englished

        total = data_filtered.shape[0]
        data_filtered =  data_filtered[(data_filtered['honest'] == 'on')]
        ## filter gibberish
        print "Removing Not Honest"
        dishonest = data_filtered.shape[0]
        # print total-dishonest

        total = data_filtered.shape[0]
        data_filtered =  data_filtered[(data_filtered['awareness'] != 'blind')]
        ## filter gibberish
        print "Removing unaware"
        not_aware = data_filtered.shape[0]
        # print total-not_aware

        total = data_filtered.shape[0]
        data_filtered =  data_filtered[(data_filtered['with_who_1'].notnull())]
        ## filter gibberish
        print "Removing Not answer"
        not_answer = data_filtered.shape[0]
        # print total-not_answer

        total = data_filtered.shape[0]
        data_filtered =  data_filtered[(data_filtered['with_who_2'].notnull())]
        ## filter gibberish
        print "Removing Not answer"
        not_answer = data_filtered.shape[0]
        # print total-not_answer
        # print "Total"
        # print total

        data_filtered = self.data.copy(deep=True)


        data_filtered =  data_filtered[
            ## filter gibberish
            (data_filtered['gibberish'] == True) &
            ## Returns  the none random
            (data_filtered['academic'] < 3) &
            ## Returns the ones that are being honest
            # (data_filtered['honest'] == 'on') &
            # (data_filtered['field'] == 'LS') &
            (data_filtered['field'] != '') &
            (data_filtered['tongue'] == 'skilled') &
            (data_filtered['awareness'] != 'blind') &
            # (data_filtered['awareness'] != 'avoid') &

            # (data_filtered['time_1'].notnull()) &
            # (data_filtered['ease_1'].notnull()) &
            # (data_filtered['support_1'].notnull()) &
            # (data_filtered['regret_1'].notnull()) &
            (data_filtered['with_who_1'].notnull())
        ]



        self.data = data_filtered
        return data_filtered

    def code_when_to_num_cat(self, t, w):


        w = str(w)
        # print w

        if w == 'nan':
            return w

        if t == 'cite DataLabour':
            return w

        if t == 'Jam Share Data':
            if w == 'later':
            # if w == 'later' or w == '10y' or w == '1y' or w == '6m':
                return '10y'
            elif w != 'null' and type(w) is not float:
                # print (type(w))
                # release = datetime.datetime.strptime(w, "%d/%m/%Y").date()
                release = datetime.datetime.strptime(w, "%m/%Y").date()
                today = date.today()
                grace_period = abs(release - today)
                # print grace_period.days
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

        return r


    def code_awareness(self):
        df = self.data.copy(deep=True)

        def check_awareness(row):
            r = str(row)

            data = (r).split(',')
            PATTERN = re.compile(r"""([^'una, \[\]])""",re.UNICODE)

            y = map(lambda x: re.search(PATTERN, x), data)

            def traverse(o, tree_types=(list, tuple)):
                if isinstance(o, tree_types):
                    for value in o:
                        for subvalue in traverse(value):
                            if subvalue != None:
                                yield subvalue.group()
                else:
                    yield o



            y = list(traverse(y))
            y = map(int,y)

            y = set(y)

            if set([1,3]).issubset(y):
                a = 'full'
            elif 3 in y:
                a = 'publication'
            elif 4 in y:
                a = 'blind'
            elif 1  in y:
                a = 'half'
            else:
                a = 'avoid'
            # print a

            assert type(a) is str
            return a


        df['awareness'] = df.apply(lambda row: check_awareness(row['awareness']), axis=1)
        self.data = df


    def code_ways(self):
        df = self.data.copy(deep=True)

        def check_ways(row):
            r = str(row)

            data = (r).split(',')
            PATTERN = re.compile(r"""([^'una, \[\]])""",re.UNICODE)

            y = map(lambda x: re.search(PATTERN, x), data)

            def traverse(o, tree_types=(list, tuple)):
                if isinstance(o, tree_types):
                    for value in o:
                        for subvalue in traverse(value):
                            if subvalue != None:
                                yield subvalue.group()
                else:
                    yield o



            y = list(traverse(y))
            y = map(int,y)

            y = set(y)
            # print y
            a = ""
            if set([1]).issubset(y):
                a = 'e-mail'
            if set([1]).issubset(y) and (set([2]).issubset(y) or set([3]).issubset(y)):
                a = 'multi'
            elif set([2]).issubset(y) or set([3]).issubset(y):
                a = 'self-depositing'
            if set([4]).issubset(y):
                a = 'Never'
            # if set([empty]).issubset(y) in y:
            #     a = 'avoid'
            # print a
            return a


        df['ways'] = df.apply(lambda row: check_ways(row['ways']), axis=1)
        self.data = df

    #
    # def code_ways(self):
    #     df = self.data.copy(deep=True)
    #
    #     def add_lang_skill(row):
    #         r = pd.Series(row).fillna("0")
    #
    #         r = r.replace(["1","2","3","4"],[1,2,3,4])
    #         # r = r.replace(["1","2","3","4"],["request","open_repository","inst_repository","i_dont"])
    #         print r.shape
    #         # if r.count() >= 2:
    #         #     a = 'skilled'
    #         # else:
    #         #     a = 'unskilled'
    #         # return a
    #
    #
    #     df['ways'] = df.apply(lambda row: add_lang_skill(row['ways']), axis=1)


    def code_tongue(self):
        df = self.data.copy(deep=True)

        def add_lang_skill(row):
            r = str(row)


            data = (r).split(',')
            PATTERN = re.compile(r"""([^'|"\[u]+[\w\W][^'|"\[u]+)""",re.UNICODE)

            y = map(lambda x: re.search(PATTERN, x), data)

            def traverse(o, tree_types=(list, tuple)):
                if isinstance(o, tree_types):
                    for value in o:
                        for subvalue in traverse(value):
                            if subvalue != None:
                                yield subvalue.group()
                else:
                    yield o

            y = list(traverse(y))
            y =pd.Series(y)

            y = y.replace(["I'm a native English speaker",
                           "I have lived in an English speaking country for more than 2 years",
                           "I have been living in an English speaking country for at least 10 months",
                           "I've learnt English when I was a child ( > 12 years old)",
                           "I have an English proficiency above professional working level"],[9,6,2,5,1])
            if y.sum() >= 2:
                a = 'skilled'
            else:
                a = 'unskilled'
            return a


        df['tongue'] = df.apply(lambda row: add_lang_skill(row['tongue']), axis=1)
        self.data = df


    def code_trust(self):
        df = self.data.copy(deep=True)

        df['trust'] = df['trust'].replace(['first','second'],[df['treatment_eval_1'],df['treatment_eval_2']])
        self.data = df



    def code_survey_numeric(self):
        df = self.data.copy(deep=True)


        df['when_to_1'] = df.apply(lambda row: self.code_when_to_num_cat(row['treatment_eval_1'], row['when_to_1']), axis=1)
        df['when_to_2'] = df.apply(lambda row: self.code_when_to_num_cat(row['treatment_eval_2'], row['when_to_2']), axis=1)

        # df['treatment_eval_1'].replace(['Jam Share Data','cite DataLabour'],['0','1'])
        # df['treatment_eval_2'].replace(['Jam Share Data','cite DataLabour'],['0','1'])
        # self.data['with_who_1'] = self.data['with_who_1'].replace(['private','collaborators','stakeholders','public'],[1,2,3,4])
        # self.data['with_who_2'] = self.data['with_who_2'].replace(['private','collaborators','stakeholders','public'],[1,2,3,4])
        df['support_1'] = df['support_1'].replace([1,2,3,4,5],['Strongly Disagree','Disagree','Neither', 'Agree','Strongly Agree'])
        df['support_2'] = df['support_2'].replace([1,2,3,4,5],['Strongly Disagree','Disagree','Neither', 'Agree','Strongly Agree'])
        df['ease_1'] = df['ease_1'].replace([1,2,3,4,5],['Strongly Disagree','Disagree','Neither', 'Agree','Strongly Agree'])
        df['ease_2'] = df['ease_2'].replace([1,2,3,4,5],['Strongly Disagree','Disagree','Neither', 'Agree','Strongly Agree'])
        df['time_1'] = df['time_1'].replace([1,2,3,4,5],['Strongly Disagree','Disagree','Neither', 'Agree','Strongly Agree'])
        df['time_2'] = df['time_2'].replace([1,2,3,4,5],['Strongly Disagree','Disagree','Neither', 'Agree','Strongly Agree'])
        df['regret_1'] = df['regret_1'].replace([1,2,3,4,5],['Strongly Disagree','Disagree','Neither', 'Agree','Strongly Agree'])
        df['regret_2'] = df['regret_2'].replace([1,2,3,4,5],['Strongly Disagree','Disagree','Neither', 'Agree','Strongly Agree'])
        df['discipline'] = df['discipline'].apply(lambda row: row.lower())

        df['updating'] = df['updating'].fillna('not')

        # self.code_ways()
        # self.code_trust()
        # self.code_tongue()

        # df['when_best'] = df['when_best'].replace(['+10 years after publication of a peer-review paper',
        #                                '+5 years after publication of a peer-review paper',
        #                                '+3 years after publication of a peer-review paper',
        #                                '+1 years after publication of a peer-review paper',
        #                                'immediately after publication of a peer-review paper',
        #                                'before publication of a peer-review paper'],['10y+','10y','5y','3y','1y','6m'])

        # self.data['when_best'].replace(["I'm a native English speaker",
        #                                'I have lived in an English speaking country for more than 2 years',
        #                                'I have been living in an English speaking country for at least 10 months',
        #                                "I've learnt English when I was a child ( > 12 years old)"
        #                                'I have an English proficiency above professional working level'],[1,3,5,7,9])
        # df = df.replace(['cite DataLabour','Jam Share Data'],['A','B'])

        self.data_for_plots = df
        return df


    def code_for_stat_ana(self):

        xf = self.data.copy(deep=True)


        xf['when_to_1'] = xf.apply(lambda row: self.code_when_to_num_cat(row['treatment_eval_1'], row['when_to_1']), axis=1)

        xf['when_to_2'] = xf.apply(lambda row: self.code_when_to_num_cat(row['treatment_eval_2'], row['when_to_2']), axis=1)


        xf = xf.replace(['cite DataLabour','Jam Share Data'],['B','A'])
        # df['treatment_eval_1'] = df['treatment_eval_1'].replace(['Jam Share Data','cite DataLabour'],['0','1'])
        # df['treatment_eval_2'] = df['treatment_eval_1'].replace(['Jam Share Data','cite DataLabour'],['0','1'])
        xf['with_who_1'] = xf['with_who_1'].replace(['private','collaborators','stakeholders','public'],[1,2,3,4])
        xf['with_who_2'] = xf['with_who_2'].replace(['private','collaborators','stakeholders','public'],[1,2,3,4])



        self.data_for_analy = xf

        # print xf.shape
        return xf


    def compute_usability_metric(self):

        # self.code_survey_numeric()
        df = self.get_data()
        # print df.shape
        df['usability_2'] = df.apply(lambda row: np.median([row['ease_2'],row['support_2'],row['time_2']]), axis=1)
        df['usability_1'] = df.apply(lambda row: np.median([row['ease_1'],row['support_1'],row['time_1']]), axis=1)
        # MODE is not a good measure of centrality for ordinal data
        # df['usability_2'] = df.apply(lambda row: mode([row['ease_2'],row['support_2'],row['time_2']])[0][0], axis=1)
        # df['usability_1'] = df.apply(lambda row: mode([row['ease_1'],row['support_1'],row['time_1']])[0][0], axis=1)
        # print "New Usability Columns"
        # print df.shape

        self.data = df
        return df


    def get_rm_ws_dataframe(self):

        """
            This creates a data frame with structure to do a repeated methods within subject study

        :return:
        """

        def sepa_trt(row):
            r=''
            if row['variable'] == 'with_who_1':
                r = row['treatment_eval_1']
            if row['variable'] == 'with_who_2':
                r = row['treatment_eval_2']
            return r


        def add_seq(row):

            r_1 = ''
            r_2 = ''
            if row['treatment_eval_1'] == 'A':
                r_1 = 'A'
            if row['treatment_eval_1'] == 'B':
                r_1 = 'B'
            if row['treatment_eval_2'] == 'B':
                r_2 = 'B'
            if row['treatment_eval_2'] == 'A':
                r_2 = 'A'
            return r_1+r_2


        # self.code_survey_numeric()
        df = self.get_anadata()


        # print df.shape

        ###Droping missing records
        df = df[['treatment_eval_1','treatment_eval_2','with_who_1','with_who_2']].dropna()
        df['id']= df.index.values
        # print 'rm_ws_dataframe - Droping missing records'
        # print df.shape


        ###Remove missing data
        df = df[df.treatment_eval_1 != df.treatment_eval_2]
        # print 'rm_ws_dataframe - remove missing data '
        # print df.shape

        ## get random sample for when models are not same size
        # rows = random.sample(df.index, 24)
        # df_10 = df.ix[rows]
        # df = df_10

        df['seq'] = df.apply(lambda row: add_seq(row), axis=1)
        s = pd.melt(df, id_vars=['treatment_eval_1', 'treatment_eval_2','seq','id'])
        s['trt'] = s.apply(lambda row: sepa_trt(row), axis=1)

        s = s.replace(['with_who_1','with_who_2'],['1','2'])
        s = s.sort(columns=['seq','variable'])

        r = s[['value','trt','seq','variable','id']]
        r.columns = ['response','trt','sequ','period','id']
        r = r.drop_duplicates()

        # r['response'] = r['response'].replace(['private','collaborators','stakeholders','public'],[1,2,3,4])

        r[['response','trt','sequ','period','id']].to_csv('repated_meas_df',index=False, header=False)
        # print 'rm_ws_dataframe - no duplicates '
        # print df.shape

        self.check_rule_oten(r)

        return r


    def get_rm_ws_usability_dataframe(self, data):

        """
            This creates a data frame with structure to do a repeated methods within subject study

        :return:
        """

        def sepa_trt(row):
            r=''
            if row['variable'] == 'usability_1':
                r = row['treatment_eval_1']
            if row['variable'] == 'usability_2':
                r = row['treatment_eval_2']
            return r


        def add_seq(row):

            r_1 = ''
            r_2 = ''
            if row['treatment_eval_1'] == 'A':
                r_1 = 'A'
            if row['treatment_eval_1'] == 'B':
                r_1 = 'B'
            if row['treatment_eval_2'] == 'B':
                r_2 = 'B'
            if row['treatment_eval_2'] == 'A':
                r_2 = 'A'
            return r_1+r_2


        # self.code_survey_numeric()
        df = data
        # df = self.get_anadata()


        # print df.shape

        ###Droping missing records
        df = df[['treatment_eval_1','treatment_eval_2','usability_1','usability_2']].dropna()
        df['id']= df.index.values
        # print 'rm_ws_dataframe - Droping missing records'
        # print df.shape


        ###Remove missing data
        df = df[df.treatment_eval_1 != df.treatment_eval_2]
        # print 'rm_ws_dataframe - remove missing data '
        # print df.shape

        ## get random sample for when models are not same size
        # rows = random.sample(df.index, 24)
        # df_10 = df.ix[rows]
        # df = df_10

        df['seq'] = df.apply(lambda row: add_seq(row), axis=1)
        s = pd.melt(df, id_vars=['treatment_eval_1', 'treatment_eval_2','seq','id'])
        s['trt'] = s.apply(lambda row: sepa_trt(row), axis=1)

        s = s.replace(['usability_1','usability_2'],['1','2'])
        s = s.sort(columns=['seq','variable'])

        r = s[['value','trt','seq','variable','id']]
        r.columns = ['response','trt','sequ','period','id']
        r = r.drop_duplicates()

        # r['response'] = r['response'].replace(['private','collaborators','stakeholders','public'],[1,2,3,4])

        r[['response','trt','sequ','period','id']].to_csv('repated_meas_df',index=False, header=False)
        # print 'rm_ws_dataframe - no duplicates '
        # print df.shape
        return r

    def get_rm_ws_df(self, measure_1, measure_2):

        """
            This creates a data frame with structure to do a repeated methods within subject study

        :return:
        """

        def sepa_trt(row):
            r=''
            if row['variable'] == measure_1:
                r = row['treatment_eval_1']
            if row['variable'] == measure_2:
                r = row['treatment_eval_2']
            return r


        def add_seq(row):

            r_1 = ''
            r_2 = ''
            if row['treatment_eval_1'] == 'A':
                r_1 = 'A'
            if row['treatment_eval_1'] == 'B':
                r_1 = 'B'
            if row['treatment_eval_2'] == 'B':
                r_2 = 'B'
            if row['treatment_eval_2'] == 'A':
                r_2 = 'A'
            return r_1+r_2


        # self.code_survey_numeric()
        # df = data
        df = self.get_anadata()


        # print df.shape

        ###Droping missing records
        df = df[['treatment_eval_1','treatment_eval_2',measure_1,measure_2]].dropna()
        df['id']= df.index.values
        # print 'rm_ws_dataframe - Droping missing records'
        # print df.shape


        ###Remove missing data
        df = df[df.treatment_eval_1 != df.treatment_eval_2]
        # print 'rm_ws_dataframe - remove missing data '
        # print df.shape

        ## get random sample for when models are not same size
        # rows = random.sample(df.index, 24)
        # df_10 = df.ix[rows]
        # df = df_10

        df['seq'] = df.apply(lambda row: add_seq(row), axis=1)
        s = pd.melt(df, id_vars=['treatment_eval_1', 'treatment_eval_2','seq','id'])
        s['trt'] = s.apply(lambda row: sepa_trt(row), axis=1)

        s = s.replace([measure_1,measure_2],['1','2'])
        s = s.sort(columns=['seq','variable'])

        r = s[['value','trt','seq','variable','id']]
        r.columns = ['response','trt','sequ','period','id']
        r = r.drop_duplicates()

        # r['response'] = r['response'].replace(['private','collaborators','stakeholders','public'],[1,2,3,4])

        r[['response','trt','sequ','period','id']].to_csv('repated_meas_df',index=False, header=False)
        # print 'rm_ws_dataframe - no duplicates '
        # print r.shape

        self.check_rule_oten(r)

        return r


    def get_rm_ws_dataframe_whent(self):

        """
            This creates a data frame with structure to do a repeated methods within subject study

        :return:
        """

        def sepa_trt(row):
            r=''
            if row['variable'] == 'when_to_1':
                r = row['treatment_eval_1']
            if row['variable'] == 'when_to_2':
                r = row['treatment_eval_2']
            return r


        def add_seq(row):

            r_1 = ''
            r_2 = ''
            if row['treatment_eval_1'] == 'A':
                r_1 = 'A'
            if row['treatment_eval_1'] == 'B':
                r_1 = 'B'
            if row['treatment_eval_2'] == 'B':
                r_2 = 'B'
            if row['treatment_eval_2'] == 'A':
                r_2 = 'A'
            return r_1+r_2


        # self.code_survey_numeric()
        df = self.get_anadata()
        # print df.shape
        # print "sasa"

        ###Droping missing records
        df = df[['treatment_eval_1','treatment_eval_2','when_to_1','when_to_2']]
        df['id']= df.index.values
        # print df.shape


        ###Remove missing data
        df = df[df.treatment_eval_1 != df.treatment_eval_2]
        # print df.shape

        df['seq'] = df.apply(lambda row: add_seq(row), axis=1)
        s = pd.melt(df, id_vars=['treatment_eval_1', 'treatment_eval_2','seq','id'])
        s['trt'] = s.apply(lambda row: sepa_trt(row), axis=1)

        s = s.replace(['when_to_1','when_to_2'],['1','2'])
        s = s.sort(columns=['seq','variable'])

        r = s[['value','trt','seq','variable','id']]
        r.columns = ['response','trt','sequ','period','id']
        r = r.drop_duplicates()

        # r['response'] = r['response'].replace(['private','collaborators','stakeholders','public'],[1,2,3,4])


        r[['response','trt','sequ','period','id']].to_csv('repated_meas_df',index=False, header=False)
        # print r.shape
        return r







    def get_between_subject_dataframe(self, period):

        period_measure = 'Error'
        if period == 2:
            period_measure = 'with_who_2'
        if period == 1:
            period_measure = 'with_who_1'



        def add_seq2(row):
            r_1=''
            if row['treatment_eval_1'] == 'A':
                r_1 = 'AB'
            if row['treatment_eval_1'] == 'B':
                r_1 = 'BA'
            return r_1


        df = self.get_anadata()
        # print df.shape

        df['id']= df.index.values
        df['seq'] = df.apply(lambda row: add_seq2(row), axis=1)


        df_wx = df[['with_who_1','with_who_2','seq','id']]
        df_fwx = pd.melt(df_wx, id_vars=['seq','id'])
        df_fwx  = df_fwx.sort(columns=['seq','variable','id'])


        df_fwxAB = df_fwx[(df_fwx['seq'] == 'AB') & (df_fwx['variable'] == period_measure)]
        df_fwxBA = df_fwx[(df_fwx['seq'] == 'BA') & (df_fwx['variable'] == period_measure)]
        # w_toSas = df_fwx[df_fwx['variable'] == 'with_who_1']

        t = df_fwxAB['value'].value_counts()
        c = df_fwxBA['value'].value_counts()
        dd = pd.DataFrame({'t' : t, 'c':c}).fillna(0)

        # w_toSas.to_csv('between_data',index=False)

        return dd


    def get_between_subject_dataframe_whent(self, period=''):

        period_measure = 'Error'
        if period == '2':
            period_measure = 'when_to_2'
        if period == '1':
            period_measure = 'when_to_1'



        def add_seq2(row):
            r_1=''
            if row['treatment_eval_1'] == 'A':
                r_1 = 'AB'
            if row['treatment_eval_1'] == 'B':
                r_1 = 'BA'
            return r_1


        df = self.get_anadata()
        # print df.shape

        df['id']= df.index.values
        # df['seq'] = df.apply(lambda row: add_seq2(row), axis=1)


        df_wx = df[['when_to_1','when_to_2','treatment_eval_1','treatment_eval_2','id']]

        df_wx = df_wx.replace(['10y','later','3y','1y','6m'],[10,10,3,2,1])
        # print df_wx

        df_wx = df_wx[df_wx.when_to_1 != 'null']
        df_wx = df_wx[df_wx.when_to_2 != 'null']

        # print df_wx[(df_wx['treatment_eval_1'] == 'A')]

        df_fwx = pd.melt(df_wx, id_vars=['id','treatment_eval_1','treatment_eval_2'])
        df_fwx  = df_fwx.sort(columns=['variable','id'])

        # print df_fwx[(df_fwx['treatment_eval_1'] == 'A')]

        df_fwxAB = df_fwx[(df_fwx['treatment_eval_1'] == 'A') & (df_fwx['variable'] == period_measure)]
        df_fwxBA = df_fwx[(df_fwx['treatment_eval_1'] == 'B') & (df_fwx['variable'] == period_measure)]

        if period == '':
            df_fwxAB = df_fwx[(df_fwx['treatment_eval_1'] == 'A')]
            df_fwxBA = df_fwx[(df_fwx['treatment_eval_1'] == 'B')]

        # w_toSas = df_fwx[df_fwx['variable'] == 'with_who_1']

        t = df_fwxAB['value'].value_counts()
        c = df_fwxBA['value'].value_counts()
        dd = pd.DataFrame({'t' : t, 'c':c}).fillna(0)

        # w_toSas.to_csv('between_data',index=False)

        return dd


    def get_rm_ws_dataframe_scenarios(self, data = None):

        """
            This creates a data frame with structure to do a repeated methods within subject study

        :return:
        """

        def sepa_trt(row):
            r=''
            if row['variable'] == 'with_who_1':
                r = row['treatment_eval_1']
            if row['variable'] == 'with_who_2':
                r = row['treatment_eval_2']
            return r


        def add_seq(row):

            r_1 = ''
            r_2 = ''
            if row['treatment_eval_1'] == 'A':
                r_1 = 'A'
            if row['treatment_eval_1'] == 'B':
                r_1 = 'B'
            if row['treatment_eval_2'] == 'B':
                r_2 = 'B'
            if row['treatment_eval_2'] == 'A':
                r_2 = 'A'
            return r_1+r_2


        # self.code_survey_numeric()

        # if data.isnull() :
        #     df = self.get_anadata()
        # else:
        df = data



        # print df.shape
        # print "sasa"

        ###Droping missing records
        df = df[['treatment_eval_1','treatment_eval_2','with_who_1','with_who_2','scenario']].dropna()
        df['id']= df.index.values
        # print df.shape


        ###Remove missing data
        df = df[df.treatment_eval_1 != df.treatment_eval_2]
        # print df.shape

        ## get random sample for when models are not same size
        # rows = random.sample(df.index, 24)
        # df_10 = df.ix[rows]
        # df = df_10


        df['seq'] = df.apply(lambda row: add_seq(row), axis=1)
        s = pd.melt(df, id_vars=['treatment_eval_1', 'treatment_eval_2','seq','id','scenario'])
        s['trt'] = s.apply(lambda row: sepa_trt(row), axis=1)

        s = s.replace(['with_who_1','with_who_2'],['1','2'])
        s = s.sort(columns=['seq','variable'])

        r = s[['value','trt','seq','variable','id','scenario']]
        r.columns = ['response','trt','sequ','period','id','scenario']
        r = r.drop_duplicates()

        # r['response'] = r['response'].replace(['private','collaborators','stakeholders','public'],[1,2,3,4])


        r[['response','trt','sequ','period','id','scenario']].to_csv('repated_meas_scenario',index=False, header=False)
        # print r.shape
        return r



    def test_add_source(self,df1, df2):
        df = pd.concat([df1, df2])
        df = df.reset_index(drop=True)
        df_gpby = df.groupby(list(df.columns))
        idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
        print df.reindex(idx)


    def add_survey_data(self, rm_ws_dataframe, var):
        rm_ws_dataframe[var] = rm_ws_dataframe.apply(lambda row: self.data.loc[str(row['id']),var], axis=1)
        return rm_ws_dataframe


    def check_rule_oten(self, rm_ws_dataframe):
        from statsmodels.graphics.mosaicplot import mosaic
        d = rm_ws_dataframe.response.value_counts()
        print d

        return True

    def generate_random_ws_df(self,n):

        if n%2!=0:
            print "Number has to be even"

        j = np.random.randint(90,2560, size=n/2)
        ab = np.chararray((n/4, ), itemsize=2)
        ab[:] = 'AB'
        ba = np.chararray((n/4, ), itemsize=2)
        ba[:] = 'BA'
        xx = np.append(ab,ba)
        yy = np.append(ab,ba)
        idx      = pd.Series(np.append(j,j))
        response = pd.Series(np.random.randint(1,5, size=n))
        response = pd.Series(np.random.randint(1,5, size=n))
        # sequ     = pd.Series(np.random.choice(['AB','BA'], size=n))
        sequ     = pd.Series(np.append(xx,xx))
        # period   = pd.Series(np.random.randint(1,3, size=n))
        period   = pd.Series(np.append(np.ones((n/2,), dtype=np.int), np.full((n/2, ), 2, dtype=np.int)))
        # trt      = pd.Series(np.random.choice(['A','B'], size=n))

        def separate(p,s):
            t = 0
            if p == 1:
                t = s[0][0]
            if p == 2:
                t = s[1][0]
            return t

        data_simu = pd.DataFrame({'response':response,'period':period,'sequ':sequ, 'id':idx})
        data_simu['trt'] = data_simu.apply(lambda row: separate(row['period'], row['sequ']), axis=1)
        data_simu = data_simu.sort(['sequ','period','trt'])


        data_simu.head(5)
        data_simu.response.value_counts().plot(kind='bar')
        data_simu = data_simu.dropna()
        return data_simu


# if __name__ == '__main__':
# # init('logs/data_incremental_file')
#
# fc = FrameExperimentTable('logs/data_incremental_file')
# # fc = FrameExperimentTable('logs/data_scenario_changed')
# fc.add_records_w_scenario('logs/data_two_records','1')
# # fc.add_records_csv('logs/data_scramble_filled_csv.csv')
# fc.add_records_w_scenario('logs/data_scenario_changed','2')
# fc.filter_noise()
#
# fc.code_survey_numeric()
# fc.code_for_stat_ana()
# xx = fc.get_rm_ws_dataframe()
# dx = fc.add_survey_data(xx,'year_born')
# print dx

# df = fc.get_between_subject_dataframe_whent('')
# df = fc.get_rm_ws_dataframe_whent()
# ll= fc.get_rm_ws_dataframe_scenarios()

# # print ll

# c = FrameExperimentTable('logs/data_scenario_changed')
# c.filter_noise()
# c.code_for_stat_ana()
# c.code_survey_numeric()
# new_data = c.get_rm_ws_dataframe()
#
# data_n =  c.generate_random_ws_df(53)
# print data_n
# # ss = np.chararray((46/2, ), itemsize=2)
# # ss[:] = 'AB'
# # print ss

# print data_n.sort(['id','period']).reset_index()
