import django
django.setup()

import random
from django.utils import timezone
import pickle
# from django.contrib.auth.models import User
from publytics.models import Bar, CheckIn
from myglobals import END_HOUR, START_HOUR, MINS_PER_CHUNK, AGE_RANGES, DEMO_YEAR, DEMO_MONTH, DEMO_START_DAY_OF_MONTH

TOTAL_CHUNKS = (END_HOUR+24 - START_HOUR) * (60 / MINS_PER_CHUNK)

bars = { 'Ten Forward'             : '75226', # zipcodes are same, but would not be in practice
         'Taffey\'s Snake Pit Bar' : '75226',
         'Sister Louisa\'s Church' : '75226',
         'Mos Eisley Cantina'      : '75226',
         'Trees'                   : '75226',
         'new Bar'                 : '75226',
         'myBar'                   : '75226',
         'this.bar'                : '75226',
         'Foo Bar'                 : '75226',
         'Dada'                    : '75226'
       }

# Initialize output collections to zero
genderValues = {}
ageValues = {}
timeValues = {}
for bar in bars.keys():
    for tc in range(0, TOTAL_CHUNKS):
        genderValues[(bar, True, tc)] = 0
        genderValues[(bar, False, tc)] = 0
        timeValues[(bar, tc)] = 0
        for ac in range(0, len(AGE_RANGES)):
            ageValues[(bar, ac, tc)] = 0


def lookupAgeIndex(age):
    count = 0
    for lower,upper in AGE_RANGES:
        if age >= lower and age < upper:
            return count
        count += 1
    return None

def create_checkins(name, zipcode):
    myBar = Bar(name=name, zipcode=zipcode)
    myBar.save()

    for checkin in range(0, 100):        
        isMale = False if random.random() > 0.44 else True # bias to female checkins
        age = int(random.triangular(low = 21, high= 50, mode = 23))
        # or, weighted distribution with conditionals using map defined by Nick
        
        # 7 hours from 8 to 3, assume arrivals more likely in the earlier part of the interval
        hour = START_HOUR + int(random.gauss(mu = 0.4, sigma = .25) * (24 + END_HOUR - START_HOUR))

        if hour < START_HOUR:
            hour = START_HOUR
        elif hour >= END_HOUR + 24:
            hour = END_HOUR + 23

        timeChunk = (hour - START_HOUR) * (60 / MINS_PER_CHUNK)
        hour = hour - 24 if hour >= 24 else hour # adjust for rollover

        # assume arrivals more likely in the earlier part of the hour
        minute = random.randint(0, 59)

        time = timezone.datetime(
            DEMO_YEAR, DEMO_MONTH, 
            DEMO_START_DAY_OF_MONTH if hour >= START_HOUR else DEMO_START_DAY_OF_MONTH+1, hour, minute)

        timeChunk += minute / MINS_PER_CHUNK
        
        ageIndex = lookupAgeIndex(age)
        for tc in range(timeChunk, TOTAL_CHUNKS):
            genderValues[(name, isMale, tc)] += 1
            ageValues[(name, ageIndex, tc)] += 1
        timeValues[(name, timeChunk)] += 1

        myCheckIn = CheckIn(isMale=isMale, age=age, bar=myBar, created_at=time)
        myCheckIn.save()

for name, zipcode in bars.items():
    create_checkins(name, zipcode)

pickle.dump( genderValues, open( "gender.p", "wb" ) )
pickle.dump( ageValues, open( "age.p", "wb" ) )
pickle.dump( timeValues, open( "time.p", "wb" ) )