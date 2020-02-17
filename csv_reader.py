import csv
import pprint

filepath = "/Users/aarondelossantos/Desktop/Course Syllabus and Schedule/Week 21.csv"
possibleSchedTypes = ("A", "B", "C", "D", "E", "F", "G")

def extractData(filepath):
    print("processing")

    csvReader = csv.DictReader(open(filepath,mode='r', encoding='utf-8-sig'))

    nestedDict = {}
    print("preparing nested dict")

    for counter, row in enumerate(csvReader):
        nestedDict[counter] = dict(row)

    return nestedDict

def findScheduleType(scheduleType, dataSource):
    print("Finding schedule type")
    siftedDict = {}
    for key in dataSource:
        if dataSource[key]["Schedule type"] == scheduleType:
            siftedDict[key] = dataSource[key]
    return siftedDict

if __name__ == '__main__':
    extractedData = extractData(filepath)
    pprint.pprint(extractedData[1]["Subject"])
    scheduleA = findScheduleType("A", extractedData)
    print(scheduleA)