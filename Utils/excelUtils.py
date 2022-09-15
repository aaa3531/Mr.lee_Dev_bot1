import csv

def getColumnData(csvFile, columnNo):
    data = []
    rdr = csv.reader(csvFile)
    for line in rdr:
        data.append(line[columnNo])
    return data

def getKrxData(csvFile):
    data = []
    rdr = csv.reader(csvFile)
    for line in rdr:
        data.append((line[2], line[1]))
    return data