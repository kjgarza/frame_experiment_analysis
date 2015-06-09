__author__ = 'kristian'


import sys
import json
import pandas as pd


## Takes file from logger and transforms into a table for R analysis

def main(fn, output):
    exposures = []
    outcomes = []
    awareness_evaluation = inputs = create_1 = create_2 = first_evaluation = second_evaluation = {}

    with open(fn) as f:
        for line in f:
            obj = json.loads(line)
            if obj['inputs']:
                sessionid = obj['inputs']['sessionid']
                discipline = obj['inputs']['discipline']

                if obj['event'] == 'exposure':
                    # p = obj['params']
                    # for params in obj['params'].iteritems():
                        # print params
                        # print sessionid
                        # print params[1]['name']
                    try:
                        inputs = {
                            'sessionid': sessionid,
                            'session':          sessionid,
                            'discipline': discipline,
                            'year_born': obj['inputs']['year_born'],
                            'materials_type': obj['inputs']['materials_type'],
                            'howmany': obj['inputs']['howmany'],
                            # 'when_best': obj['inputs']['when_best'],
                            # 'ways': obj['inputs']['ways'],
                            # 'frequency': obj['inputs']['frequency'],
                            # 'updating': obj['inputs']['updating'],
                            # 'tongue': obj['inputs']['tongue'],
                            'time_exposure': obj['time'],
                            'treatment': obj['params']['template1']['name'],
                            # 'template2': params[1]['name'],
                            }
                    except:
                        inputs = {
                            'sessionid': sessionid,
                            'session':          sessionid,
                            'discipline': discipline,
                            'year_born': obj['inputs']['year_born'],
                            'materials_type': obj['inputs']['materials_type'],
                            'howmany': obj['inputs']['howmany'],
                            # 'when_best': obj['inputs']['when_best'],
                            # 'frequency': obj['inputs']['frequency'],
                            # 'updating': 0,
                            # 'tongue': 0,
                            # 'ways': 0,
                            'time_exposure': obj['time'],
                            'treatment': obj['params']['template1']['name'],
                            # 'template2': params[1]['name'],
                            }
                if obj['event'] == 'create':
                    if bool(create_1) == False :
                    # for variables, k in obj['extra_data'].iteritems():
                    #     print obj['extra_data']['data_file_title']
                        create_1 = {
                            'sessionid': sessionid,
                            'time_create': obj['time'],
                            'with_who_1': obj['extra_data']['with_who'],
                            'when_to_1': obj['extra_data']['when_to'],
                            'data_file_title_1': obj['extra_data']['data_file_title'],
                        }
                    else:
                    # for variables, k in obj['extra_data'].iteritems():
                    #     print obj['extra_data']['data_file_title']
                        create_2 = {
                            'sessionid': sessionid,
                            'time_create': obj['time'],
                            'with_who_2': obj['extra_data']['with_who'],
                            'when_to_2': obj['extra_data']['when_to'],
                            'data_file_title_2': obj['extra_data']['data_file_title'],
                        }
                elif obj['event'] == 'first_evaluation':
                    # for variables, k in obj['extra_data'].iteritems():
                    #     print obj['extra_data']['data_file_title']
                    try:
                        first_evaluation = {
                            'sessionid': sessionid,
                            'time_first_evaluation': obj['time'],
                            'support_1': obj['extra_data']['support'],
                            'time_1': obj['extra_data']['time'],
                            'ease_1': obj['extra_data']['ease'],
                            'regret_1': obj['extra_data']['regret'],
                        }
                    except:
                        first_evaluation = {
                            'sessionid': sessionid,
                            'time_first_evaluation': obj['time'],
                            'support_1': obj['extra_data']['support'],
                            'time_1': obj['extra_data']['time'],
                            'ease_1': obj['extra_data']['ease'],
                            'regret_1': 0,
                        }
                elif obj['event'] == 'second_evaluation':
                    # for variables, k in obj['extra_data'].iteritems():
                    #     print obj['extra_data']['data_file_title']
                    try:
                        second_evaluation = {
                            'sessionid': sessionid,
                            'time_second_evaluation': obj['time'],
                            'support_2': obj['extra_data']['support'],
                            'time_2': obj['extra_data']['time'],
                            'ease_2': obj['extra_data']['ease'],
                            'regret_2': obj['extra_data']['regret'],
                        }
                    except:
                        second_evaluation = {
                            'sessionid': sessionid,
                            'time_second_evaluation': obj['time'],
                            'support_2': obj['extra_data']['support'],
                            'time_2': obj['extra_data']['time'],
                            'ease_2': obj['extra_data']['ease'],
                            'regret_2': 0,
                        }
                elif obj['event'] == 'awareness_evaluation':
                    # for variables, k in obj['extra_data'].iteritems():
                    #     print obj['extra_data']['data_file_title']
                    awareness_evaluation = {
                            'sessionid': sessionid,
                            'time_awareness_evaluation': obj['time'],
                            'academic': obj['extra_data']['academic'],
                            'trust': obj['extra_data']['trust'],
                            'awareness': obj['extra_data']['awareness'],
                            'honest': obj['extra_data']['honest'],
                            'when_best': obj['extra_data']['when_best'],
                            'ways': obj['extra_data']['ways'],
                            'frequency': obj['extra_data']['frequency'],
                            'updating': obj['extra_data']['updating'],
                            'man_hours': obj['extra_data']['man_hours'],

                     }


            if bool(awareness_evaluation) and bool(inputs) and bool(create_1) and bool(create_2) and bool(first_evaluation) and bool(second_evaluation):

                z = dict(awareness_evaluation.items() + inputs.items() + create_1.items() + create_2.items() +
                        first_evaluation.items() +
                        second_evaluation.items()
                )
                outcomes.append(z)
                awareness_evaluation = inputs = create_1 = create_2 = first_evaluation = second_evaluation = {}
    outcomes.append(dict(create_1.items()))
    o = pd.DataFrame(outcomes).set_index(['sessionid'])

    o.to_csv(output)


def second_extract(fn, output):
    awareness_evaluation = []
    second_evaluation = []
    first_evaluation = []
    create_1 = []
    create_2 = []
    with open(fn) as f:
        for line in f:
            obj = json.loads(line)
            # sessionid = obj['inputs']['sessionid']

            # if obj['event'] == 'exposure':
            #     p = obj['params']
            #     for position, (sk, source) in enumerate(zip(p['story_keys'], p['sources'])):
            #         exposures.append({
            #             'sessionid': sessionid,
            #             'position': position,
            #             'story_key': sk,
            #             'source': source,
            #             })

            if obj['event'] == 'second_evaluation':
                # print obj['extra_data']
                # for sessionid in obj['extra_data'].iteritems():
                second_evaluation.append({
                    'sessionid': obj['extra_data']['sessionid'],
                    # 'story_key': int(sk),
                    'support_2':  obj['extra_data']['support'],
                    'time_2':     obj['extra_data']['time'],
                    'ease_2':     obj['extra_data']['ease'],
                    'regret_2':   obj['extra_data']['regret'],
                    'time_second_evaluation': obj['time'],
                    'discipline': obj['extra_data']['inputs']['discipline'],
                    'treatment_eval_2':obj['extra_data']['treatment'],
                    # 'man_hours':  obj['extra_data']['inputs']['man_hours'],
                    # 'howmany':    obj['extra_data']['inputs']['howmany'],
                    # 'year_born':  obj['extra_data']['inputs']['year_born'],
                    # 'materials_type':  obj['extra_data']['inputs']['materials_type'],
                    # 'tongue':     obj['extra_data']['inputs']['tongue'],
                })
            elif obj['event'] == 'first_evaluation':
                # print obj['extra_data']
                # for sessionid in obj['extra_data'].iteritems():
                first_evaluation.append({
                    'sessionid': obj['extra_data']['sessionid'],
                    # 'story_key': int(sk),
                    'time_first_evaluation': obj['time'],
                    'support_1':  obj['extra_data']['support'],
                    'time_1':     obj['extra_data']['time'],
                    'ease_1':     obj['extra_data']['ease'],
                    'regret_1':   obj['extra_data']['regret'],
                    'treatment_eval_1':obj['extra_data']['treatment'],
                    'discipline': obj['extra_data']['inputs']['discipline'],

                })

            elif obj['event'] == 'awareness_evaluation':
                # print obj['extra_data']
                # for sessionid in obj['extra_data'].iteritems():
                awareness_evaluation.append({
                    'sessionid':        obj['extra_data']['sessionid'],
                    'session':          obj['extra_data']['sessionid'],
                    'time_awareness_evaluation': obj['time'],
                    'academic':         obj['extra_data']['academic'],
                    'trust':            obj['extra_data']['trust'],
                    'awareness':        obj['extra_data']['awareness'],
                    'honest':           obj['extra_data']['honest'],
                    'when_best':        obj['extra_data']['when_best'],
                    'ways':             obj['extra_data']['ways'],
                    'frequency':        obj['extra_data']['frequency'],
                    'updating':         obj['extra_data']['updating'],
                    'discipline':       obj['extra_data']['inputs']['discipline'],
                    'tongue':           obj['extra_data']['inputs']['tongue'],
                    'year_born':        obj['extra_data']['inputs']['year_born'],
                    'materials_type':   obj['extra_data']['inputs']['materials_type'],
                    'howmany':          obj['extra_data']['inputs']['howmany'],
                    'man_hours':        obj['extra_data']['inputs']['man_hours'],


                })
            elif obj['event'] == 'create':
                # print obj['extra_data']
                # for sessionid in obj['extra_data'].iteritems():
                if obj['extra_data']['trial'] == 0:
                    create_1.append({
                        'sessionid':       obj['extra_data']['sessionid'],
                        'time_create_1':   obj['time'],
                        'with_who_1':      obj['extra_data']['with_who'],
                        'treatment_1':     obj['extra_data']['treatment'],
                        'when_to_1':       obj['extra_data']['when_to'],
                        'trial_1':         obj['extra_data']['trial'],
                        'data_file_title_1': obj['extra_data']['data_file_title'],
                        'discipline':        obj['extra_data']['inputs']['discipline'],

                    })
                else:
                    create_2.append({
                        'sessionid':       obj['extra_data']['sessionid'],
                        'time_create_2':   obj['time'],
                        'with_who_2':      obj['extra_data']['with_who'],
                        'treatment_2':     obj['extra_data']['treatment'],
                        'trial_2':         obj['extra_data']['trial'],
                        'when_to_2':       obj['extra_data']['when_to'],
                        'data_file_title_2': obj['extra_data']['data_file_title'],
                        'discipline':        obj['extra_data']['inputs']['discipline'],

                    })



    a = pd.DataFrame(second_evaluation).set_index(['sessionid','discipline'])
    b = pd.DataFrame(first_evaluation).set_index(['sessionid','discipline'])
    c = pd.DataFrame(create_1).set_index(['sessionid','discipline'])
    d = pd.DataFrame(awareness_evaluation).set_index(['sessionid','discipline'])
    f = pd.DataFrame(create_2).set_index(['sessionid','discipline'])
    # o = pd.DataFrame(first_evaluation).set_index(['sessionid'])
    # o = pd.DataFrame(first_evaluation).set_index(['sessionid'])
    # print a
    a.join(b).join(c).join(d).join(f).to_csv(output)
    # o.to_csv(output)


def jsontocsv(fn, output):
    import json
    import csv
    f = open(fn)
    data = json.load(f)
    f.close()

    f= csv.writer(open(output,'wb+'))

    for item in data:
        f.writerow([item['pk'], item['model']] + item['fields'].values())


def using_r():
    from rpy2.robjects.packages import importr
    import rpy2.robjects as ro
    ro.r('x=c()')
    ro.r('x[1]=22')
    ro.r('x[2]=44')
    print(ro.r('x'))


def datatoFrame(fn, output, method):

    if method == 'old':
        main(fn, output)
    elif method == 'new':
        second_extract(fn, output)

    # main(fn, output)

    mydict = pd.DataFrame.from_csv(output, sep=',', index_col=0)

    return mydict

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
    # datatoFrame('logs/delete_input_inextra', 'dummy4')
    # jsontocsv('logs/data_two_records', 'dummy3')
