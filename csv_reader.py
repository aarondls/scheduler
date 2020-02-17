import csv
import pprint

filepath = "/Users/aarondelossantos/Desktop/Course Syllabus and Schedule/Full Schedule.csv"
possibleSchedTypes = ("A", "B", "C", "D", "E", "F", "G")

def extractData(filepath):
    print("processing")

    csvReader = csv.DictReader(open(filepath,mode='r', encoding='utf-8-sig'))

    nestedDict = {}
    print("preparing nested dict")

    for schedType in possibleSchedTypes:
        nestedDict[schedType] = {}

    for counter, row in enumerate(csvReader):
        counter = len(nestedDict[dict(row)["Schedule type"]])
        nestedDict[dict(row)["Schedule type"]][counter] = dict(row)

    return nestedDict

if __name__ == '__main__':
    extractedData = extractData(filepath)
    pprint.pprint(extractedData)