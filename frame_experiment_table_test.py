__author__ = 'kristian'

from frame_experiment_table import FrameExperimentTable

c = FrameExperimentTable('logs/data_scenario_changed')
c.filter_noise()
c.code_for_stat_ana()
c.code_survey_numeric()




def code_tongue_test():
    c.code_tongue()
    print c.get_data()["tongue"]



# c.code_awareness()

# print c.get_data()["awareness"]