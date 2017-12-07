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

graph = GraphAPI(access.fb_token)

hood = graph.get('hoodsite/posts?limit=100')

print (hood)




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
