import sys

infile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')

for line in infile:
    line = line.strip().split(',')
    line.insert(1, '80')
    outline = ','.join(line)
    outfile.write(outline + '\n')
