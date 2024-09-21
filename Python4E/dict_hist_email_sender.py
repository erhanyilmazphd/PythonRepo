"""
*** Write a program to read through the mbox-short.txt and figure out who has sent the greatest number of mail messages.
The program looks for 'From ' lines and takes the second word of those lines as the person who sent the mail.
The program creates a Python dictionary that maps the sender's mail address to a count of the number of times they appear in the file.
After the dictionary is produced, the program reads through the dictionary using a maximum loop to find the most prolific committer.
"""

name = input("Enter file:")
if len(name) < 1:
    name = "./mbox-short.txt"
fhandle = open(name)

counts = dict()
for line in fhandle:
    if line.startswith("From ") :
        words = line.split()
        counts[words[1]] = counts.get(words[1], 0) + 1

max_freq_sender = None  # use of None
max_freq_count = None
for sender, count in counts.items():  # use of two iteration variable with item() method

    if max_freq_count is None or count > max_freq_count:
        max_freq_sender = sender
        max_freq_count = count

print(max_freq_sender, counts[max_freq_sender])