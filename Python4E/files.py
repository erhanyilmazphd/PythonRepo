# Use the file name mbox-short.txt as the file name
#fname = input("Enter file name: ")
#fh = open(fname)

fh = open("mbox-short.txt")

line_cnt = 0
total = 0.0
for line in fh:
    if not line.startswith("X-DSPAM-Confidence:"):
        continue

    line_s = line.rstrip()
    print(line_s)

    line_cnt += 1
    ind = line_s.find(":")
    total += float(line_s[ind+2:])

print(f"Average spam confidence: {total / line_cnt}")