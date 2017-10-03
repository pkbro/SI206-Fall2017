import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup


url = input("Enter URL: ")
list_index = int(input("Enter index: "))
count = int(input("Enter count: "))
html = urllib.request.urlopen(url).read()
name_list = []
for i in range(count):
    soup = BeautifulSoup(html,"html.parser")
    a_tag = [x for x in soup('a') if list_index == soup('a').index(x)]
    name_list.append(a_tag[0].string)
    new_url = a_tag[0].get('href')
    html = urllib.request.urlopen(new_url).read()

print (name_list[-1])
