import csv
import pprint

filepath = "/Users/aarondelossantos/Desktop/Course Syllabus and Schedule/Week 21.csv"

def extractData(filepath):
    print("processing")

    csvReader = csv.DictReader(open(filepath,mode='r', encoding='utf-8-sig'))

    nestedDict = {}
    print("preparing nested dict")

    for counter, row in enumerate(csvReader):
        nestedDict[counter] = dict(row)

    return nestedDict

if __name__ == '__main__':
    extractedData = extractData(filepath)
    pprint.pprint(extractedData[1]["Subject"])