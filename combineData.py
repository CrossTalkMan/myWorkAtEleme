#!/usr/bin/python

"""
to search each of the folders in order to combine different \
data collected from different period of time together.
@author Yuchen Liu
"""

import os
import openfile


def prepare_dirs():
    dirs = os.listdir('/users/liuyuchen/eleme')
    dirs = dirs[3:]

    num = []
    for i in range(len(dirs)):
        if os.path.isfile('/users/liuyuchen/eleme/' + dirs[i]):
            num.append(i)
    num.sort(reverse=True)

    for i in range(len(num)):
        del dirs[num[i]]
    return dirs


# return a list of list, in which noted dirs from the same day
def data_from_same_day(dirs):
    divided_dirs = []  # contains a list of list, in which noted dirs from the same day
    sub_list = []  # contains dirs' name from the same day
    current_day = dirs[0][:8]

    for i in range(len(dirs)):
        if dirs[i][:8] == current_day:
            sub_list.append(dirs[i])
        else:
            divided_dirs.append(sub_list)
            sub_list = [dirs[i]]
            current_day = dirs[i][:8]

    return divided_dirs


def combine(name, dirs):
    D = {'name': name, 'date': dirs[0][:8], 'pointCount': 0, 'values': []}
    for i in range(len(dirs)):
        try:
            files = os.listdir('/users/liuyuchen/eleme/' + dirs[i])  # get all .txts in current folder
            for j in range(len(files)):
                if name == files[j][:-13]:  # find the target file
                    with open('/users/liuyuchen/eleme/'
                                + dirs[i]
                                + "/"
                                + files[j], mode='r') as f:
                        fr = f.readlines()  # dict liked str
                        dfr = eval(fr[0])
                        D['pointCount'] += dfr['pointCount']
                        start_time = dfr['startTime']
                        end_time = dfr['endTime']
                        step = (end_time-start_time) / dfr['pointCount']
                        for k in range(len(dfr['points']['values'])):
                            if dfr['points']['values'][k] is None:
                                # a relatively small number to avoid div zero
                                dfr['points']['values'][k] = 0.01
                            D['values'].append((start_time + k*step, dfr['points']['values'][k]))
        except:
            continue
    return D


def get_result():
    all_dirs = prepare_dirs()
    divided_dirs = data_from_same_day(all_dirs)
    all_data = openfile.get_train_data()

    Data = []
    group_names = list(all_data.keys())
    for i in range(len(group_names)):
        for j in range(len(divided_dirs)):
            Data.append(combine(group_names[i], divided_dirs[j]))
    with open('result.txt', 'w') as f:
        f.write(str(Data))
    return Data


if __name__ == '__main__':
    get_result()
