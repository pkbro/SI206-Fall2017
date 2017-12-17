import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
from pylab import *
from plotly.graph_objs import *
import plotly.graph_objs as go
import plotly
import json
import sqlite3
import requests
import urllib
import access
from facepy import GraphAPI
import json
from datetime import datetime
import calendar

#Set the credentials for plotly use
plotly.tools.set_credentials_file(username='pkbro', api_key=access.plotly_key)

#Initialize a graph object to access the Facebook GraphAPI Explorer
graph = GraphAPI(access.fb_token,version='2.8')


#Facebook cache file setup
CACHE_FNAME = "fb_cache.json"
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION_fb = json.loads(cache_contents)
except:
    CACHE_DICTION_fb = {}

#Instagram cache file setup
CACHE_FNAME_2 = "insta_cache.json"
try:
    cache_file = open(CACHE_FNAME_2,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION_insta = json.loads(cache_contents)
except:
    CACHE_DICTION_insta = {}

#Github cahce file setup
CACHE_FNAME_3 = "git_cache.json"
try:
    cache_file = open(CACHE_FNAME_3,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION_git = json.loads(cache_contents)
except:
    CACHE_DICTION_git = {}

# fb_post_info, insta_data, and git_data are all lists that end up being written
# to their respective cache files. The reason each of them start with a dictionary
# of the days of the week with time breakdown was because I initially figured it
# would be simplest to access this organized data from the cache file, but later
# decided against it.

fb_post_info = [{'Sunday':{'6':0,'12':0,'18':0,'24':0},'Monday':{'6':0,'12':0,'18':0,'24':0},'Tuesday':{'6':0,'12':0,'18':0,'24':0},'Wednesday':{'6':0,'12':0,'18':0,'24':0},'Thursday':{'6':0,'12':0,'18':0,'24':0},'Friday':{'6':0,'12':0,'18':0,'24':0},'Saturday':{'6':0,'12':0,'18':0,'24':0}}]

#get_fb_posts checks the cache file to see if the necessary data is already present
#and if not, makes a call to the Facebook API and writes the desired data to the
#cache. In both cases, the cached data is returned. I used Addy Osmani's account
#because I only had 9 posts on Facebook and it aligned better with my github call.
def get_fb_posts():
    if 'addy' in CACHE_DICTION_fb:
        print("using cache for fb")
    else:
        print("fetching for fb")
        res = graph.get('articlesfordevelopers/posts?limit=100')
        for x in res['data']:
            info_dict = {}
            if 'message' in x:
                info_dict['message'] = x['message']
            else:
                info_dict['message'] = x['story']

            info_dict['id'] = x['id']

            adjust_time = x['created_time'].replace('-'," ")
            adjust_time2 = adjust_time.replace("T"," ")
            dt_obj = datetime.strptime(adjust_time2[:19], '%Y %m %d %H:%M:%S')
            day = calendar.day_name[dt_obj.weekday()]
            for y in fb_post_info[0].keys():
                if day == y:
                    if int(adjust_time2[11:13]) < 6:
                        fb_post_info[0][day]['6'] += 1
                        info_dict['time'] = '6'
                        break
                    elif int(adjust_time2[11:13]) < 12:
                        fb_post_info[0][day]['12'] += 1
                        info_dict['time'] = '12'
                        break
                    elif int(adjust_time2[11:13]) < 18:
                        fb_post_info[0][day]['18'] += 1
                        info_dict['time'] = '18'
                        break
                    else:
                        fb_post_info[0][day]['24'] += 1
                        info_dict['time'] = '24'
                        break

            info_dict['day'] = day

            r = graph.get(x['id'] + '?fields=likes.limit(0).summary(true)')
            info_dict['likes'] = r['likes']['summary']['total_count']
            fb_post_info.append(info_dict)
        try:
            CACHE_DICTION_fb['addy'] = fb_post_info
            dumped_json_cache = json.dumps(CACHE_DICTION_fb)
            fw = open(CACHE_FNAME, 'w')
            fw.write(dumped_json_cache)
            fw.close()
        except:
            print("Not valid")

    return CACHE_DICTION_fb['addy']


insta_data = [{'Sunday':{'6':0,'12':0,'18':0,'24':0},'Monday':{'6':0,'12':0,'18':0,'24':0},'Tuesday':{'6':0,'12':0,'18':0,'24':0},'Wednesday':{'6':0,'12':0,'18':0,'24':0},'Thursday':{'6':0,'12':0,'18':0,'24':0},'Friday':{'6':0,'12':0,'18':0,'24':0},'Saturday':{'6':0,'12':0,'18':0,'24':0}}]
#This function is nearly identical to get_fb_posts. It grabs my personal instagram
#data. This is limited to only grabbing 20 posts per Instagram's rules.
def get_insta_posts():
    if 'me' in CACHE_DICTION_insta:
        print("using cache for insta")

    else:
        print('fetching for insta')
        r = requests.get('https://api.instagram.com/v1/users/self/media/recent/?access_token='+access.instagram_password)

        for x in r.json()['data']:
            post_info = {}
            post_info['id'] = x['id']
            post_info['likes'] = x['likes']['count']
            post_info['comments'] = x['comments']['count']

            time = datetime.fromtimestamp(int(x['created_time'])).isoformat()
            adjust_time = time.replace('-'," ")
            adjust_time2 = adjust_time.replace("T"," ")
            dt_obj = datetime.strptime(adjust_time2[:19], '%Y %m %d %H:%M:%S')
            day = calendar.day_name[dt_obj.weekday()]
            post_info['day'] = day
            for y in insta_data[0].keys():
                if day == y:
                    if int(adjust_time2[11:13]) < 6:
                        insta_data[0][day]['6'] += 1
                        post_info['time'] = '6'
                        break
                    elif int(adjust_time2[11:13]) < 12:
                        insta_data[0][day]['12'] += 1
                        post_info['time'] = '12'
                        break
                    elif int(adjust_time2[11:13]) < 18:
                        insta_data[0][day]['18'] += 1
                        post_info['time'] = '18'
                        break
                    else:
                        insta_data[0][day]['24'] += 1
                        post_info['time'] = '24'
                        break

            insta_data.append(post_info)

        try:
            CACHE_DICTION_insta['me'] = insta_data
            dumped_json_cache = json.dumps(CACHE_DICTION_insta)
            fw = open(CACHE_FNAME_2, 'w')
            fw.write(dumped_json_cache)
            fw.close()
        except:
            print("Not valid")

    return CACHE_DICTION_insta['me']



git_data = [{'Sunday':{'6':0,'12':0,'18':0,'24':0},'Monday':{'6':0,'12':0,'18':0,'24':0},'Tuesday':{'6':0,'12':0,'18':0,'24':0},'Wednesday':{'6':0,'12':0,'18':0,'24':0},'Thursday':{'6':0,'12':0,'18':0,'24':0},'Friday':{'6':0,'12':0,'18':0,'24':0},'Saturday':{'6':0,'12':0,'18':0,'24':0}}]
#This function is nearly identical to get_fb_posts. It grabs Addy Osmani's last
# 100 github repositories and data on them.
def get_git_info():
    if 'addy' in CACHE_DICTION_git:
        print('using cache for git')
    else:
        print('fetching for git')
        r = requests.get('https://api.github.com/users/addyosmani/repos?page=1&per_page=100')

        for x in r.json():
            repo_data = {}
            repo_data['id'] = x['id']
            repo_data['stars'] = x['stargazers_count']

            adjust_time = x['created_at'].replace('-'," ")
            adjust_time2 = adjust_time.replace("T"," ")
            dt_obj = datetime.strptime(adjust_time2[:19], '%Y %m %d %H:%M:%S')
            day = calendar.day_name[dt_obj.weekday()]
            repo_data['day'] = day
            for y in git_data[0].keys():
                if day == y:
                    if int(adjust_time2[11:13]) < 6:
                        git_data[0][day]['6'] += 1
                        repo_data['time'] = '6'
                        break
                    elif int(adjust_time2[11:13]) < 12:
                        git_data[0][day]['12'] += 1
                        repo_data['time'] = '12'
                        break
                    elif int(adjust_time2[11:13]) < 18:
                        git_data[0][day]['18'] += 1
                        repo_data['time'] = '18'
                        break
                    else:
                        git_data[0][day]['24'] += 1
                        repo_data['time'] = '24'
                        break

            git_data.append(repo_data)


        try:
            CACHE_DICTION_git['addy'] = git_data
            dumped_json_cache = json.dumps(CACHE_DICTION_git)
            fw = open(CACHE_FNAME_3, 'w')
            fw.write(dumped_json_cache)
            fw.close()
        except:
            print("Not valid")

    return CACHE_DICTION_git['addy']


#Create db file
conn = sqlite3.connect('final_DB.sqlite')
cur = conn.cursor()

#Facebook table creation and assignment of data to table
fb_posts = get_fb_posts()[1:]
# my_fb = get_my_fb()[1:]

cur.execute('DROP TABLE IF EXISTS FB')

cur.execute('CREATE TABLE FB (post_id TEXT, message TEXT, day TEXT, time TEXT, likes NUMBER)')


for x in fb_posts:
    post_tup = (x['id'],x['message'],x['day'],x['time'],x['likes'])
    cur.execute('INSERT INTO FB (post_id, message, day, time, likes) VALUES (?,?,?,?,?)', post_tup)

# for x in my_fb:
#     post_tup = (x['id'],x['message'],x['day'],x['time'],x['likes'])
#     cur.execute('INSERT INTO FB (post_id, message, day, time, likes) VALUES (?,?,?,?,?)', post_tup)

conn.commit()



#Instagram table creation and assignment of data to table
insta_info = get_insta_posts()[1:]

cur.execute('DROP TABLE IF EXISTS INSTA')
cur.execute('CREATE TABLE INSTA (post_id TEXT, day TEXT, time TEXT, likes NUMBER, comments NUMBER)')

for x in insta_info:
    post_tup = (x['id'],x['day'], x['time'], x['likes'], x['comments'])
    cur.execute('INSERT INTO INSTA (post_id, day, time, likes, comments) VALUES (?,?,?,?, ?)', post_tup)

conn.commit()


#Github table creation and assignment of data to table
git_info = get_git_info()[1:]

cur.execute('DROP TABLE IF EXISTS GIT')
cur.execute('CREATE TABLE GIT (post_id TEXT, day TEXT, time TEXT, stars NUMBER)')

for x in git_info:
    post_tup = (x['id'],x['day'],x['time'],x['stars'])
    cur.execute('INSERT INTO GIT (post_id, day, time, stars) VALUES (?,?,?,?)', post_tup)

conn.commit()


#1st Visualization: Creating a bar chart of when Addy Osmani has posted his last
# 100 posts on Facebook. This is broken down by 4 time intervals throughout each
#day of the week.
sun = list(cur.execute('SELECT time FROM FB WHERE day = "Sunday"'))
mon = list(cur.execute('SELECT time FROM FB WHERE day = "Monday"'))
tue = list(cur.execute('SELECT time FROM FB WHERE day = "Tuesday"'))
wed = list(cur.execute('SELECT time FROM FB WHERE day = "Wednesday"'))
thu = list(cur.execute('SELECT time FROM FB WHERE day = "Thursday"'))
fri = list(cur.execute('SELECT time FROM FB WHERE day = "Friday"'))
sat = list(cur.execute('SELECT time FROM FB WHERE day = "Saturday"'))

#This function takes one of the above lists of day times and returns a list of
#organized time counts for that day, ex: day_iterate(sun) hypothetically returns
#[4,6,9,5] corresponding to the number of posts in the four time intervals,
#chronologically ordered.
def day_iterate(day):
    early = 0
    mid_early = 0
    late = 0
    very_late = 0
    for x in day:
        if x[0] == '6':
            early += 1
        elif x[0] == '12':
            mid_early += 1
        elif x[0] == '18':
            late += 1
        else:
            very_late += 1

    return([early,mid_early,late,very_late])

sunday = day_iterate(sun)
monday = day_iterate(mon)
tuesday = day_iterate(tue)
wednesday = day_iterate(wed)
thursday = day_iterate(thu)
friday = day_iterate(fri)
saturday = day_iterate(sat)


#Filling data for the four time intervals across each day.
fb0 = go.Bar(
    x=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],

    y= [sunday[0], monday[0], tuesday[0], wednesday[0], thursday[0], friday[0], saturday[0]],
    name='12am - 6am',
    marker=dict(
        color='rgb(49,130,189)'
    )
)
fb1 = go.Bar(
    x=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    y=[sunday[1], monday[1], tuesday[1], wednesday[1], thursday[1], friday[1], saturday[1]],
    name = '6am - 12pm',
    marker=dict(
        color='rgb(200,90,140)',
    )
)
fb2 = go.Bar(
    x=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    y=[sunday[2], monday[2], tuesday[2], wednesday[2], thursday[2], friday[2], saturday[2]],
    name='12pm - 6pm',
    marker=dict(
        color='rgb(100,30,189)'
    )
)
fb3 = go.Bar(
    x=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    y=[sunday[3], monday[3], tuesday[3], wednesday[3], thursday[3], friday[3], saturday[3]],
    name='6pm - 12am',
    marker=dict(
        color='rgb(20,204,204)',
    )
)

data = [fb0, fb1, fb2, fb3]
#Graph design
layout = go.Layout(
    title = 'Addy Osmani: Facebook Post Times',
    titlefont = dict(
            family = 'Futura',
            color  = '#34495e'
        ),
    legend=dict(
            font=dict(
                family='Futura',
                color='#34495e'
            ),
            bgcolor='#E0E0E0',
            bordercolor='#16A085',
            borderwidth=2
    ),
    xaxis = dict(
        title = 'Day of Post',
        titlefont = dict(
            family = 'Futura',
            color  = '#34495e'
        ),
        tickfont = dict(
            family = 'Futura',
            color  = '#34495e'
        )
    ),
    yaxis = dict(
        title = 'Number of Posts',
        titlefont = dict(
            family = 'Futura',
            color  = '#34495e'
        ),
        tickfont = dict(
            family = 'Futura',
            color  = '#34495e'
        )
    )

)

fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='text-bar')

#2nd Visualization: Line Chart comparing Addy Osmani's average likes per Facebook
#post for each day of the week vs. his average stargazer count per repository for
#each day of the week(based on day repo was created).
weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
git_sun = list(cur.execute('SELECT stars FROM GIT WHERE day = "Sunday"'))
git_mon = list(cur.execute('SELECT stars FROM GIT WHERE day = "Monday"'))
git_tue = list(cur.execute('SELECT stars FROM GIT WHERE day = "Tuesday"'))
git_wed = list(cur.execute('SELECT stars FROM GIT WHERE day = "Wednesday"'))
git_thu = list(cur.execute('SELECT stars FROM GIT WHERE day = "Thursday"'))
git_fri = list(cur.execute('SELECT stars FROM GIT WHERE day = "Friday"'))
git_sat = list(cur.execute('SELECT stars FROM GIT WHERE day = "Saturday"'))

fb_sun = list(cur.execute('SELECT likes FROM FB WHERE day = "Sunday"'))
fb_mon = list(cur.execute('SELECT likes FROM FB WHERE day = "Monday"'))
fb_tue = list(cur.execute('SELECT likes FROM FB WHERE day = "Tuesday"'))
fb_wed = list(cur.execute('SELECT likes FROM FB WHERE day = "Wednesday"'))
fb_thu = list(cur.execute('SELECT likes FROM FB WHERE day = "Thursday"'))
fb_fri = list(cur.execute('SELECT likes FROM FB WHERE day = "Friday"'))
fb_sat = list(cur.execute('SELECT likes FROM FB WHERE day = "Saturday"'))

git_day_data = [git_sun,git_mon,git_tue,git_wed,git_thu,git_fri,git_sat]
#Finding average star count
avg_stars = []
for x in git_day_data:
    star_sum = 0
    for y in x:
        star_sum += y[0]
    avg_stars.append(star_sum/len(x))


fb_day_data = [fb_sun,fb_mon,fb_tue,fb_wed,fb_thu,fb_fri,fb_sat]
#Finding average like count
avg_likes = []
for x in fb_day_data:
    like_sum = 0
    for y in x:
        like_sum += int(y[0])
    avg_likes.append(like_sum/len(x))

#Fill in Github line data
git_line = go.Scatter(
    x = weekdays,
    y = avg_stars,
    line = dict(
        color = ('rgb(70, 145, 100)'),
        width = 4),
    name = "Avg. Stars Per Repository (Github)"
)

#Fill in FB line data
fb_line = go.Scatter(
    x = weekdays,
    y = avg_likes,
    line = dict(
        color = ('rgb(140, 80, 100)'),
        width = 4),
    name = "Avg. Likes Per Post (Facebook)"
)

data = [git_line, fb_line]
#Graph Design
layout = dict(
            title = 'Addy Osmani: Avg. Star Count vs Avg. Like Count',
            titlefont = dict(
                    family = 'Futura',
                    color  = '#34495e'
                ),
            legend=dict(
                    font=dict(
                        family='Futura',
                        color='#34495e'
                    ),
                    bgcolor='#E0E0E0',
                    bordercolor='#16A085',
                    borderwidth=2
            ),
            xaxis = dict(
                title = 'Weekday',
                titlefont = dict(
                    family = 'Futura',
                    color  = '#34495e'
                ),
                tickfont = dict(
                    family = 'Futura',
                    color  = '#34495e'
            )),
            yaxis = dict(
                title = 'Avg. Star and Like Count',
                titlefont = dict(
                    family = 'Futura',
                    color  = '#34495e'
                ),
                tickfont = dict(
                    family = 'Futura',
                    color  = '#34495e'
            ))
        )
fig = dict(data=data,layout=layout)
py.plot(fig,filename='styled-line')


#3rd Visualization: Table output using pandas to display the 20 posts I was able
#receive from the Instagram API and their likes, comments, and average likes per comments.
insta_stats = cur.execute('SELECT * from INSTA')
insta_stats = cur.fetchall()

instagram_dicts = []
for x in insta_stats:
    instagram_dicts.append({'Avg. Likes Per Comment':(x[3]/x[4]),'Comments':x[4],'Likes':x[3]})

df = pd.DataFrame(instagram_dicts)
print (df)

cur.close()
