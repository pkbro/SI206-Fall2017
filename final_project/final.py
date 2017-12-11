import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import sqlite3
import requests
import urllib
import networkx as nx
import access
from facepy import GraphAPI
import json
from datetime import datetime
import calendar
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions

# natural_language_understanding = NaturalLanguageUnderstandingV1(
#   username='{Phillip Brown}',
#   password= '{fw3-3nY-g4y-2NF}',
#   version='2017-02-27')
#
# response = natural_language_understanding.analyze(
#   text='IBM is an American multinational technology company '
#        'headquartered in Armonk, New York, United States, with '
#        'operations in over 170 countries.',
#   features=Features(
#     entities=EntitiesOptions(
#       emotion=True,
#       sentiment=True,
#       limit=2),
#     keywords=KeywordsOptions(
#       emotion=True,
#       sentiment=True,
#       limit=2)))
#
# print(json.dumps(response, indent=2))
graph = GraphAPI(access.fb_token,version='2.8')




CACHE_FNAME = "APIs_cache.json"
# Put the rest of your caching setup here:
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

def get_fb_posts(term):
	if term in CACHE_DICTION:
		print("using cache")
	else:
		print("fetching")
		data = graph.get('michiganfball/posts?limit=10')
		try:
			CACHE_DICTION[term] = data
			dumped_json_cache = json.dumps(CACHE_DICTION)
			fw = open(CACHE_FNAME, 'w')
			fw.write(dumped_json_cache)
			fw.close()
		except:
			print("Not valid")

	return CACHE_DICTION[user]








# n = hood['data'][0]['id']
# print(n)
# react_num = graph.get(n + '/likes')
# print (react_num)

#You need a dictionary for each id. Within each, you'll have keys for messages, likes, and comments if you can get them.
#Grab the messages, make a list, iterate and send them to nlp api to retrive sentiment scores.
fb_post_info = [{'6':0,'12':0,'18':0,'24':0},{'Sunday':0,'Monday':0,'Tuesday':0,'Wednesday':0,'Thursday':0,'Friday':0,'Saturday':0}]



#
for x in hood['data']:
    info_dict = {}
    info_dict['message'] = x['message']
    info_dict['id'] = x['id']
    info_dict['time'] = x['created_time']
    adjust_time = x['created_time'].replace('-'," ")
    adjust_time2 = adjust_time.replace("T"," ")
    if int(adjust_time2[11:13]) < 6:
        fb_post_info[0]['6'] += 1
    elif int(adjust_time2[11:13]) < 12:
        fb_post_info[0]['12'] += 1
    elif int(adjust_time2[11:13]) < 18:
        fb_post_info[0]['18'] += 1
    else:
        fb_post_info[0]['24'] += 1

    dt_obj = datetime.strptime(adjust_time2[:19], '%Y %m %d %H:%M:%S')
    day = calendar.day_name[dt_obj.weekday()]
    for y in fb_post_info[1].keys():
        if day == y:
            fb_post_info[1][y] += 1
            break
    info_dict['day'] = day


    r = graph.get(x['id'] + '?fields=likes.limit(0).summary(true)')
    info_dict['likes'] = r['likes']['summary']['total_count']
    fb_post_info.append(info_dict)



print (fb_post_info)






# fb_t = access.fb_token
# fb_page = "Hoodsite"
# graph = facebook.GraphAPI(fb_t, api_version='v2.6')
# p = graph.requests(fb_page+'/posts?limit=100')
#
# print (p)


# fb_r = requests.get("")
#
# print(fb_r)


G = nx.Graph()
edge_list = [
    ("A","B"),
    ("A","C"),
    ("A","D"),
    ("B","D"),
    ("C","B"),
    ("C","D"),
    ("A","E"),
    ("E","D"),
    ("F","A")
]
# G.add_edges_from(edge_list)
# nx.draw_networkx(G, with_labels=True)
# plt.show()
