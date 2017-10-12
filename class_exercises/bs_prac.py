from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error

url = input("Enter: ")
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
tags = soup('a')
# for tag in tags:
#     print(tag.get('href', None))

#Find and return all the h2 titles with class module title.
print (soup.title.string)
titles = soup.find_all("a", class_= "module__title__link")
for title in titles:
    print (title.string)
