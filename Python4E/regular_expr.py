
"""
Finding Numbers in a Haystack

In this assignment you will read through and parse a file with text and numbers.
You will extract all the numbers in the file and compute the sum of the numbers.

Data Files
We provide two files for this assignment.
One is a sample file where we give you the sum for your testing and the other is the actual data you need to process for the assignment.

Sample data: http://py4e-data.dr-chuck.net/regex_sum_42.txt (There are 90 values with a sum=445833)
Actual data: http://py4e-data.dr-chuck.net/regex_sum_1626566.txt (There are 86 values and the sum ends with 874)
These links open in a new window.
Make sure to save the file into the same folder as you will be writing your Python program.

Note: Each student will have a distinct data file for the assignment - so only use your own data file for analysis.

Handling The Data
The basic outline of this problem is to read the file, look for integers using the re.findall(),
looking for a regular expression of '[0-9]+' and then converting the extracted strings to integers and summing up the integers.

"""

import re

name = input("Enter file:")
if len(name) < 1:
    name = "regex_sum_1626566.txt" # "regex_sum_42.txt" # regex_sum_1626566.txt
fh = open(name)

regex = r"([0-9]+)"

if 1:
    # list comprehension
    print(sum( [int(elem) for elem in re.findall(regex, fh.read()) ]))
else :
    # Normal way
    mylist = list()
    counts = dict()
    for line in fh:
        match = re.findall(regex, line)
        #print(match)
        for elem in match:
            mylist.append(int(elem))

    print(mylist)
    print(sum(mylist))
