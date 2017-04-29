from django.utils import timezone 

# ASSUMPTIONS:
# START_HOUR is before minute and END_HOUR is after midnight
# DEMO_START_DAY_OF_MONTH is a day such that tomorrow is of same month
# MINS_PER_CHUNK is <= 60 and fits evenly into 60

AGE_RANGES = [
    (21, 25),
    (25, 30),
    (30, 40),
    (40, 50),
    (50, 130)
]

START_HOUR = 20
END_HOUR = 3
MINS_PER_CHUNK = 20
DEMO_YEAR = 2016
DEMO_MONTH = 6
DEMO_START_DAY_OF_MONTH = 6

DEMO_OPENING_TIME = timezone.datetime(2016, DEMO_MONTH, DEMO_START_DAY_OF_MONTH, START_HOUR, 0, 0)
DEMO_CLOSING_TIME = timezone.datetime(2016, DEMO_MONTH, DEMO_START_DAY_OF_MONTH+1, END_HOUR, 0, 0)