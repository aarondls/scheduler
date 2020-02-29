import csv
import pprint

filepath = "/Users/aarondelossantos/Desktop/Course Syllabus and Schedule/Full Schedule.csv"
possibleSchedTypes = ("A", "B", "C", "D", "E", "F", "G")

def extractData(filepath):
    print("Extracting events from CSV file")

    try:
        csvReader = csv.DictReader(open(filepath,mode='r', encoding='utf-8-sig'))

        nestedDict = {}

        for schedType in possibleSchedTypes:
            nestedDict[schedType] = {}

        for counter, row in enumerate(csvReader):
            counter = len(nestedDict[dict(row)["Schedule type"]])
            nestedDict[dict(row)["Schedule type"]][counter] = dict(row)
    except:
        print("Unable to import events")
        raise
    return nestedDict

extractedData = extractData(filepath)

if __name__ == '__main__':
    pprint.pprint(extractedData)