import access
import requests
import json
from datetime import datetime
import calendar
from facepy import GraphAPI
import plotly.plotly as py
from plotly.graph_objs import *
import plotly


plotly.tools.set_credentials_file(username='pkbro', api_key='7XOHtLBNyejURzFDhi5x')


trace0 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = Data([trace0, trace1])

py.plot(data, filename = 'basic-line')

# def get_git_info():
#     if 'me' in CACHE_DICTION_git:
#         print('using cache for git')
#     else:
#         print('fetching for git')
#         r = requests.get('https://api.github.com/users/pkbro/repos')
#         git_data = [{'6':0,'12':0,'18':0,'24':0},{'Sunday':0,'Monday':0,'Tuesday':0,'Wednesday':0,'Thursday':0,'Friday':0,'Saturday':0}]
#
#         for x in r.json():
#             adjust_time = x['created_at'].replace('-'," ")
#             adjust_time2 = adjust_time.replace("T"," ")
#             dt_obj = datetime.strptime(adjust_time2[:19], '%Y %m %d %H:%M:%S')
#             day = calendar.day_name[dt_obj.weekday()]
#             if int(adjust_time2[11:13]) < 6:
#                 git_data[0]['6'] += 1
#             elif int(adjust_time2[11:13]) < 12:
#                 git_data[0]['12'] += 1
#             elif int(adjust_time2[11:13]) < 18:
#                 git_data[0]['18'] += 1
#             else:
#                 git_data[0]['24'] += 1
#
#             for y in git_data[1].keys():
#                 if day == y:
#                     git_data[1][y] += 1
#                     break
#         try:
#             CACHE_DICTION_git['me'] = git_data
#             dumped_json_cache = json.dumps(CACHE_DICTION_git)
#             fw = open(CACHE_FNAME_3, 'w')
#             fw.write(dumped_json_cache)
#             fw.close()
#         except:
#             print("Not valid")
#
#     return CACHE_DICTION_git['me']
#
# insta_stuff = get_insta_posts()
# git_stuff = get_git_info()
#
# print(insta_stuff)
# print(git_stuff)

#Line chart seeing if number of likes is related to number of comments
# insta_data = []
# for x in r.json()['data']:
#     post_info = {}
#     post_info['id'] = x['id']
#     post_info['likes'] = x['likes']['count']
#     post_info['comments'] = x['comments']['count']
#     insta_data.append(post_info)

# print(insta_data)
