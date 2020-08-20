## What is Scheduler?

Scheduler takes a pre-defined schedule format in CSV, calculates which schedule type lands on which day, and uploads the corresponding events of the schedule type to Google Calendar. This allows the schedule to be viewed across different platforms that sync with Google Calendar.

Scheduler is meant to be an easy way for students (or anyone, really) to upload their schedule into Google Calendar and view it on several devices. With an *n*-day cycle of A,B,C,D,...,*N* schedule types formatted in a CSV file, Scheduler will take the provided starting schedule type, date and desired duration, then calculate which schedule type falls on which days and upload it to Google Calendar.

Scheduler can skip weekends and will advance the schedule from Friday to Monday if desired. Scheduler can also add events to separate calendars of the same name as the event, for improved appearance and organization.

With Scheduler, any schedule can be easily matched with the right dates, uploaded to Google Calendar, and viewed on multiple devices.


## Sample
For example, take this 7-day schedule of A,B,C,D,E,F,G that rotates on weekdays and skips weekends.

<p align="center">
  <img src="https://github.com/aarondls/scheduler/blob/master/Images/Reserve_schedule.png" width="550">
</p>

With this CSV file, Scheduler can gather the necessary information for each event and schedule type. Scheduler will then ask for when the desired schedule should start, which schedule type to start on, how many days to fill in the schedule, whether the schedule skips weekends, and which calendar the schedule should be uploaded to. In this example, it is uploaded to the primary (default) calendar.

<p align="center">
  <img src="https://github.com/aarondls/scheduler/blob/master/Images/schedulebot_with_aton_sched.gif" width="500">
</p>

Scheduler automatically recognizes when the cycle ends, and goes back to the first schedule type until all days have been filled with the proper schedule type. Scheduler will also skip weekends if told to do so. The created events on Google Calendar is then:

<p align="center">
  <img src="https://github.com/aarondls/scheduler/blob/master/Images/Reserve_schedule_created_1.png" width="900">
</p>

<p align="center">
  <img src="https://github.com/aarondls/scheduler/blob/master/Images/Reserve_schedule_created_2.png" width="900">
</p>

Scheduler can also upload events into separate calendars of the same name. For example, take this regular Monday to Friday (M,T,W,R,F) schedule.

<p align="center">
  <img src="https://github.com/aarondls/scheduler/blob/master/Images/UIUC_schedule.png" width="900">
</p>

This time, there are calendars named after each event, and the events should be added its corresponding calendar. For example, a calendar named "Introduction to Computing" exists, and the event "Introduction to Computing" should be uploaded to that calendar.

<p align="center">
  <img src="https://github.com/aarondls/scheduler/blob/master/Images/schedulebot_with_separated_calendars.gif" width="900">
</p>

This way, each event can have its own color, timezone, and other details. The created events on Google Calendar is then:

<p align="center">
  <img src="https://github.com/aarondls/scheduler/blob/master/Images/UIUC_schedule_created.png" width="900">
</p>

Since each calendar can have different colors, it is easy to identify each event with just a glance. With Google Calendar being synced with other devices, the schedule can be viewed on multiple devices, such as on the native Mac and iOS calendar app.

<p align="center">
  <img src="https://github.com/aarondls/scheduler/blob/master/Images/UIUC_schedule_on_Mac.png" width="900">
</p>

<p align="center">
  <img src="https://github.com/aarondls/scheduler/blob/master/Images/UIUC_schedule_on_iOS.jpeg" width="900">
</p>

## Dependencies

```shell
pip install google-api-python-client
```

## Setting up Scheduler

The CSV file can be prepared from a spreadsheet with the required columns of "Start Time", "End Time", and "Description". Other columns can be added, and will be referred to by its set name.

<p align="center">
  <img src="https://github.com/aarondls/scheduler/blob/master/Images/Reserve_schedule_excel.png" width="900">
</p>

The Excel sheet above can then be saved as a CSV file, then modify the string *filepath* in csv_reader.py with the file path of the CSV file.

```python
filepath = "/filepath/here/file.csv"
```

In the same file, modify the list *possibleSchedTypes* with the names of the schedule types as labeled in the CSV file.

```python
possibleSchedTypes = ["A", "B", "C", "D", "E", "F", "G"]
```

Authorize access to your Google Calendar. Refer to steps 1-2 [here](https://developers.google.com/calendar/quickstart/python) for guidance. In the Load.py file, modify the *credentialFile* string with the filepath of the generated Google Calendar credentials file.

```python
credentialFile = "/filepath/here/client_secret.json"
```

Then, run Load.py file once to generate a pickle file.

In the Schedulebot.py file, change the string *defaultTimeZone* to the intended timezone.

```python
defaultTimeZone = "America/Chicago"
```

## Usage

Once everything is set-up, simply run schedulebot.py.

```python
python schedulebot.py
```

Scheduler will first prompt for the starting date of the schedule, in the format m/d/yyyy.
> What is the starting date in m/d/yyyy?
If the provided date is the wrong format or doesn't exist, Scheduler will exit. This applies for every invalid input to prompts.

Scheduler will then prompt for the starting schedule type, and will display the possible choices.
> What is the starting schedule type?
> Possible schedules: M, T, W, R, F

The next prompt will ask for how long the schedule would last in days.
> How long will this schedule last in days (as a number, ie 5)?
There is no limit to how long you can enter, so please do not enter an excessively long duration.

Scheduler will then ask if it should skip weekends and move the schedule after Friday to Monday. 'y', 'Y', 'Yes', and 'yes' are acceptable answers. If the answer is none of the above choices, then Scheduler will assume it is a no.
> Does the schedule skip weekends?
> y/n
Note that if weekends are skipped, then weekends will not count towards the duration entered in the previous prompt.

The last prompt before the events can be created will ask whether the events should be added to calendars sharing the same name. Note that the calendar must exist and have the same name as the events.
> Should the events be added to the calendar of the same name? If no, events will be added to main calendar.
> y/n

If the answer is not a yes, then Scheduler will default to the primary calendar. If the answer is yes but there is no calendar that exists with the same name as the event, then Scheduler will again default to the primary calendar.
