import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import sqlite3
import requests
import urllib
import networkx as nx

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
]
G.add_edges_from(edge_list)
nx.draw_networkx(G, with_labels=True)
plt.show()
