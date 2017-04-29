from django.test import TestCase
from publytics.models import Bar, Bouncer, CheckIn
import pickle, pdb
from datetime import timedelta
from myglobals import DEMO_OPENING_TIME, AGE_RANGES, MINS_PER_CHUNK
from django.test import Client
from django.contrib.auth.models import User
import base64

class BarDemoTestCase(TestCase):

    # Has demo data for 10 bars with 100 checkins each
    fixtures = ['checkins_fixtures.json']

    def setUp(self):
        """The following contain expected test case values"""
        self.genderValues = pickle.load( open( "gender.p", "rb" ) )
        self.ageValues = pickle.load( open( "age.p", "rb" ) )
        self.timeValues = pickle.load( open( "time.p", "rb" ) )

    def test_get_todays_by_gender(self):
        """Test to make sure today's gender query works"""
        for key, checkins in self.genderValues.items():            
            barName, isMale, timeChunk = key
            time = DEMO_OPENING_TIME+timedelta(minutes=MINS_PER_CHUNK*(timeChunk+1))
            self.assertEqual(
                Bar.objects.get(name=barName).getTodaysByGender(
                    isMale, time), 
                checkins)

    def test_get_todays_by_age(self):
        """Test to make sure today's age query works"""
        for key, checkins in self.ageValues.items():
            barName, ageGroup, timeChunk = key
            time = DEMO_OPENING_TIME+timedelta(minutes=MINS_PER_CHUNK*(timeChunk+1))
            lower, upper = AGE_RANGES[ageGroup]
            self.assertEqual(
                Bar.objects.get(name=barName).getTodaysByAge(
                    lower, upper, time), 
                checkins)

    def test_get_todays_time_activity(self):
        """Test to make sure today's activity over time query works"""
        for key, checkins in self.timeValues.items():
            barName, timeChunk = key
            startTime = DEMO_OPENING_TIME+timedelta(minutes=MINS_PER_CHUNK*timeChunk)
            endTime = startTime+timedelta(minutes=MINS_PER_CHUNK)
            self.assertEqual(
                Bar.objects.get(name=barName).getTodaysTimeActivity(
                    startTime, endTime), 
                checkins)

class BarLiveTestCase(TestCase):

    def setUp(self):
        """Initialize a bouncer, which has a 1-1 relationship with Beaglebone instances"""
        username = 'sean'
        password = 'mypassword'

        self.user = User.objects.create_user(username, 'ba919@gttx.org', password)
        self.user.save()
        self.bar = Bar(name='Ten Forward', zipcode='75226')
        self.bar.save()
        self.bouncer = Bouncer(bar=self.bar, user=self.user)
        self.bouncer.save()
        self.c = Client(HTTP_AUTHORIZATION='Basic ' + base64.b64encode('%s:%s' % (username, password)))

    def test_create_underage_checkin(self):
        """Test using REST framework to check in someone underage"""
        response = self.c.post('/checkin/', {'age': 17, 'isMale': True})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(CheckIn.objects.filter(age=17, isMale=True).exists())

    def test_create_checkin(self):
        """Test using REST framework to check in someone of age"""
        response = self.c.post('/checkin/', {'age': 25, 'isMale': True})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CheckIn.objects.filter(age=25, isMale=True).exists())


