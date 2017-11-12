import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

url = input("Enter: ")
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html,"html.parser")

span_tags = soup('span')
comment_total = []
for span in span_tags:
    comment_total.append(span.string)

print(comment_total)
