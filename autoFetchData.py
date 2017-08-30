#!/usr/bin/python
"""
to get data of specific date automatically
@author Yuchen Liu
"""


import json
import requests
import os
import datetime

# groups created by administrator or included randomized data which are useless to be predict
BLACK_LIST = ['cod-lpd_cod_job_group',
              'dt_rec-waimai_ranking_group',
              'napos_goods-zeus_ers_4taobao_group_gz',
              'libra-base_rumble_group',
              'minos-lpd_alliance_group',
              'elemesearch-base_restaurantactivity_search_group_gz',
              'elemesearch-base_restaurantactivity_search_group',
              'marketing_budget-dtpush_job_group',
              'payment3-risk_group',
              'payment1-risk_group',
              'payment7-risk_group',
              'payment5-risk_group',
              'payment6-risk_group',
              'payment4-risk_group'
              'payment8-risk_group',
              'payment2-risk_group',
              'napos_payservice-napos_payservice_spark_group_gz',
              'shop_growth-waimai_ranking_search_group',
              'pps_service-dt_pps_service_group',
              'scorpio-risk_group',
              'pluto-risk_group',
              'neptune-risk_group',
              'talaris_team_clear-lpd_alliance_group',
              'biz_push-biz_push_group',
              'apollo-apollo_sos_group']


# find all group names automatically
# input: null
# output: names(list)
def get_all_group():
    group_name = []
    url = """http://trace-gw.elenet.me/api/query/dal?ql=\
            timer.dal.dashboard.group%20(0)%20by%20group%20range\
            (%2220170718%2000:00:00%22,%2220170719%2000:00:12%22)"""
    resp = requests.get(url)
    result_in_json = json.loads(resp.text)

    points = result_in_json['groupedPoints']
    points.sort(key=lambda item:item['points']['summary']['count'], reverse=True)

    with open('/Users/liuyuchen/eleme/group.txt', 'w') as f:
        for i in range(len(points)):
            if (points[i]['groupBy']['group'] not in BLACK_LIST) \
                    and ('dbadmin' not in points[i]['groupBy']['group']):
                f.write(points[i]['groupBy']['group'] + '\n')

    for i in range(len(points)):
        if (points[i]['groupBy']['group'] not in BLACK_LIST) \
                and ('dbadmin' not in points[i]['groupBy']['group']):
            group_name.append(points[i]['groupBy']['group'])

    return group_name


# prepare urls according to group name and start&end time
# input: group=group_name(str), t1=start_time(str), t2=end_time(str)
# output: url(str)
def prepare_url(group, t1, t2):
    url = []
    for i in range(len(group)):
        url.append("""http://trace-gw.elenet.me/api/query/dal?ql='counter."""
                   + group[i]
                   + """.dal_host' range("%s","%s")''"""
                   % (t1, t2))
    return url


# record data order by date and time
# input: result=well-fetched_data(dict), t1=start_time(str), t2=end_time(str)
# output: null
def write_result_into_file(result, t1, t2):
    if not os.path.exists('/Users/liuyuchen/eleme/%s to %s' % (t1, t2)):
        os.mkdir('/Users/liuyuchen/eleme/%s to %s' % (t1, t2))
    for i in range(len(result)):
        with open('/Users/liuyuchen/eleme/%s to %s/%s.txt' % (t1, t2, result[i]['metricName']), 'w') as f:
            f.write(str(result[i]))


# return a list of some specific moments of last 7 days
# input: null
# output: moments of last 7 days(list)
def get_time_list():
    time = [' 00:00:00', ' 03:00:00', ' 06:00:00', ' 09:00:00', ' 12:00:00',
            ' 15:00:00', ' 18:00:00', ' 21:00:00', ' 23:59:59']
    today = datetime.date.today()
    last_7_days = []
    for i in range(3):  # used to be 7, in order to reduce computing cost, i changed it into 3.
        tmp = []
        for j in range(len(time)):
            tmp.append((today - datetime.timedelta(days=i+1)).strftime('%Y%m%d') + time[j])
        last_7_days.append(tmp)
    return last_7_days


if __name__ == '__main__':

    date = get_time_list()
    print(date)

    result = []
    group = get_all_group()
    print(len(group))
    for i in range(len(date)):
        for j in range(len(date[i]) - 1):
            url = prepare_url(group, date[i][j], date[i][j+1])
            for k in range(len(url)):
                resp = requests.get(url[k])
                try:
                    result.append(json.loads(resp.text))
                except:
                    continue
            print(url)
            write_result_into_file(result, date[i][j], date[i][j+1])
    print('well done!')

