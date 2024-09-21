"""
Extracting Data from JSON

In this assignment you will write a Python program somewhat similar to http://www.py4e.com/code3/json2.py.
The program will prompt for a URL, read the JSON data from that URL using urllib
and then parse and extract the comment counts from the JSON data, compute the sum of the numbers in the file and enter the sum below:
We provide two files for this assignment.
One is a sample file where we give you the sum for your testing and the other is the actual data you need to process for the assignment.

Sample data: http://py4e-data.dr-chuck.net/comments_42.json (Sum=2553)
Actual data: http://py4e-data.dr-chuck.net/comments_1626571.json (Sum ends with 17)
You do not need to save these files to your folder since your program will read the data directly from the URL.

Note: Each student will have a distinct data url for the assignment - so only use your own data url for analysis.

Data Format
The data consists of a number of names and comment counts in JSON as follows:

{
  comments: [
    {
      name: "Matthias"
      count: 97
    },
    {
      name: "Geomer"
      count: 97
    }
    ...
  ]
}
The closest sample code that shows how to parse JSON and extract a list is json2.py.
You might also want to look at xml3.py to see how to prompt for a URL and retrieve data from a URL.

Sample Execution

$ python3 solution.py
Enter location: http://py4e-data.dr-chuck.net/comments_42.json
Retrieving http://py4e-data.dr-chuck.net/comments_42.json
Retrieved 2733 characters
Count: 50
Sum: 2...

"""

import urllib.request, urllib.parse
import json, ssl

#url = 'http://py4e-data.dr-chuck.net/comments_42.json'
url = 'http://py4e-data.dr-chuck.net/comments_1626571.json'

print('Retrieving', url)
uh = urllib.request.urlopen(url)
data = uh.read().decode()

try:
    js = json.loads(data)
except:
    print('==== Download error ===')
    print(data)
    quit()


#print(json.dumps(js, indent=4))

#elems = json.dumps(js['comments'])
elems = js['comments']

count = 0
summ = 0
for elem in elems:
    print('count:', elem['count'])
    count = count + 1
    summ = summ + elem['count']

print('Count:', count)
print('Sum:', summ)