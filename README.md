## What is Scheduler?
Scheduler takes a pre-defined schedule format in CSV, calculates which schedule type lands on which day, and uploads the corresponding events of the schedule type to Google Calendar. 

Scheduler is meant to be an easy way for students (or anyone, really) to upload their schedule into Google Calendar. With an *n*-day cycle of A,B,C,D,...,*N* schedule types, Scheduler will take the provided starting schedule type, date and desired duration, then calculate which schedule type falls on which days and upload it to Google Calendar. This way, schedules can be easily matched with the right dates to be synced and viewed on multiple devices.

For example, take this 7-day schedule of A,B,C,D,E,F,G:

<p align="center">
  <img src="https://github.com/aarondls/Scheduler/blob/master/Images/Full_Schedule_Excel.png" width="550">
</p>

After converting to CSV, Scheduler can then read the file and gather the necessary information for each event and schedule type. Scheduler will then ask for when the desired schedule should start, which schedule type to start on, and how many days to fill in the schedule. 

<p align="center">
  <img src="https://github.com/aarondls/Scheduler/blob/master/Images/Schedulebot-in-action.gif" width="500">
</p>

Scheduler automatically recognizes when the cycle ends, and goes back to the first schedule type until all days have been filled with the proper schedule type. The created events on Google Calendar is then:

<p align="center">
  <img src="https://github.com/aarondls/Scheduler/blob/master/Images/Schedule-created.png" width="900">
</p>


## Dependencies
```
pip install google-api-python-client
```

## Setting up Scheduler
The CSV file can be prepared with a spreadwith with the required columns of "Start Time", "End Time", and "Description". Other columns can be added, and will be referred to by its set name.

Modify the string *filepath* in csv_reader.py with the file path of the CSV file. Modify the list *possibleSchedTypes* with the names of the schedule types as labelled in the CSV file.

```python
filepath = "/filepath/here/file.csv"
possibleSchedTypes = ("A", "B", "C", "D", "E", "F", "G")
```
Modify the *credentialFile* variable in the Load.py file with the filepath of the generated Google Calendar credentials file,

```python
credentialFile = "/filepath/here/client_secret.json"
```
then run the Load.py file once to generate a pickle file.

Modify the list *possibleSchedTypes* in the schedulebot.py file with the names of the schedule types as labelled in the CSV file.

```python
possibleSchedTypes = ("A", "B", "C", "D", "E", "F", "G")
```

## Usage
Once everything is set-up, simply run schedulebot.py
