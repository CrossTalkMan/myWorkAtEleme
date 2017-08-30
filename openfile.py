#!/usr/bin/python
"""
to get group names which were already labeled
@author Yuchen Liu

'grouplabels.txt' contains group names and labels which were marked artificially
"""


def get_train_data():
    trainGroup = {}
    with open('grouplabels.txt', 'r') as f:
        fr = f.readlines()
        for i in range(len(fr)):
            fr[i] = fr[i].split()
            trainGroup[fr[i][1]] = fr[i][0]
    return trainGroup
