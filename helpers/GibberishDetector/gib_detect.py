#!/usr/bin/python

import pickle
import gib_detect_train



def detect(text):
    model_data = pickle.load(open('helpers/GibberishDetector/gib_model.pki', 'rb'))


    l = text
    # l = raw_input()
    model_mat = model_data['mat']
    threshold = model_data['thresh']
    # print gib_detect_train.avg_transition_prob(l, model_mat) > threshold
    return gib_detect_train.avg_transition_prob(l, model_mat) > threshold

