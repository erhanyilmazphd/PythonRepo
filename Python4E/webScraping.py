from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error

#url = input('Enter url - ')
url = 'http://www.dr-chuck.com'

html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve all of the anchor tags
tags = soup('a')
for tag in tags :
    print(tag.get('href', None))