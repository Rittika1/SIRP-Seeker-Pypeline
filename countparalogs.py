import sys

inputfile=sys.argv[1]

inf = open(inputfile, 'r')

countsdict = {}

for line in inf:
    if line.startswith(">"):
        SplitLine = line.split("_")
        speciesname = SplitLine[0][1:] +" " +SplitLine[1]
        if speciesname in countsdict.keys():
            countsdict[speciesname]+=1
        else:
            countsdict[speciesname]=1

for key,val in countsdict.items():
    print( key, "\t", val)