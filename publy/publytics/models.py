from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from numpy import mean, std

from myglobals import DEMO_CLOSING_TIME, DEMO_OPENING_TIME, \
    START_HOUR, END_HOUR, DEMO_YEAR, DEMO_MONTH, DEMO_START_DAY_OF_MONTH

class Bar(models.Model):
    name = models.CharField(_("name"), max_length=100)
    zipcode = models.CharField(_("zip code"), max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return str(self)

    def getTodaysByGender(self, isMale, time=None):
        return self.checkins.filter(
            created_at__gte=Bar.getOpeningTime(time), created_at__lt=Bar.getUpperTime(time), 
            isMale=isMale).count()

    def getTodaysByAge(self, lowerAge, upperAge, time=None):
        return self.checkins.filter(
            created_at__gte=Bar.getOpeningTime(time), created_at__lt=Bar.getUpperTime(time), 
            age__gte=lowerAge, age__lt=upperAge).count()

    def getTodaysTimeActivity(self, lowerTime, upperTime):
        return self.checkins.filter(created_at__gte=lowerTime, created_at__lt=upperTime).count()

    def getRank(self, time=None, info=None, myCheckins=None):
        if info:
            cStd, cAvg = info
        else:
            cStd, cAvg = Bar.getInfoByZipcode(self.zipcode, time)
        
        if not myCheckins:
            myCheckins = self.checkins.filter(
                created_at__gte=Bar.getTimeAnHourAgo(time), 
                created_at__lte=Bar.getUpperTime(time)).count()
        
        if myCheckins > cStd + cAvg:
            return 1
        elif myCheckins < cAvg - cStd:
            return -1
        else:
            return 0

    def getVolumeRank(self, info=None):
        if info:
            vStd, vAvg, bStd, bAvg = info
        else:
            vStd, vAvg, bStd, bAvg = Bar.getAudioInfoByZipcode(self.zipcode)
        
        volume = self.sensors.order_by('-created_at').first().volume
        
        if volume > vStd + vAvg:
            return 1
        elif volume < vAvg - vStd:
            return -1
        else:
            return 0

    def getBpmRank(self, info=None):
        if info:
            vStd, vAvg, bStd, bAvg = info
        else:
            vStd, vAvg, bStd, bAvg = Bar.getAudioInfoByZipcode(self.zipcode)
        
        bpm = self.sensors.order_by('-created_at').first().bpm
        
        if bpm > bStd + bAvg:
            return 1
        elif bpm < bAvg - bStd:
            return -1
        else:
            return 0

    @classmethod
    def getAudioInfoByZipcode(cls, zipcode):
        bars = cls.objects.filter(zipcode=zipcode)
        volumes = []
        bpms = []
        for bar in bars:
            reading = bar.sensors.order_by('-created_at').first()
            volumes.append(reading.volume)
            bpms.append(reading.bpm)        
        
        return std(volumes), mean(volumes), std(bpms), mean(bpms)

    @classmethod
    def generateDemoTime(cls, hours, mins):
        if hours >= START_HOUR:
            return timezone.datetime(DEMO_YEAR, DEMO_MONTH, DEMO_START_DAY_OF_MONTH, hours, mins, 0)
        else:
            return timezone.datetime(DEMO_YEAR, DEMO_MONTH, DEMO_START_DAY_OF_MONTH+1, hours, mins, 0)

    @classmethod
    def getInfoByZipcode(cls, zipcode, time=None):
        values = cls.objects.filter(
                zipcode=zipcode) \
                .annotate(num_checkins=models.Sum(
                    models.Case(
                        models.When(
                            checkins__created_at__gte=Bar.getTimeAnHourAgo(time), 
                            checkins__created_at__lte=Bar.getUpperTime(time), 
                            then=1),
                        default=0,
                        output_field=models.IntegerField()
                    ))).aggregate(models.StdDev('num_checkins'), models.Avg('num_checkins'))
        return values['num_checkins__stddev'], values['num_checkins__avg']

    @classmethod
    def now(cls, time=None):
        return time if time else timezone.now()

    @classmethod
    def getUpperTime(cls, time=None):
        if time:
            closing = cls.getClosingTime(time)
        else:
            closing = cls.getClosingTime()
            time = cls.now()
        return time if time < closing else closing

    @classmethod
    def getTimeAnHourAgo(cls, time=None):
        opening = cls.getOpeningTime(time)
        hourAgo = cls.now(time) - timedelta(hours=1)
        return opening if opening > hourAgo else hourAgo

    @classmethod
    def getClosingTime(cls, time=None):
        rightNow = cls.now(time)
        if time is not None:
            return DEMO_CLOSING_TIME
        elif rightNow.hour >= START_HOUR:
            return (rightNow + timedelta(days=1)).replace(hour=END_HOUR, minute=0)
        else:
            return rightNow.replace(hour=END_HOUR, minute=0)

    @classmethod
    def getOpeningTime(cls, time=None):
        rightNow = cls.now(time)
        if time is not None:
            return DEMO_OPENING_TIME
        elif rightNow.hour >= START_HOUR:
            return rightNow.replace(hour=START_HOUR, minute=0)
        else:
            return (rightNow - timedelta(days=1)).replace(hour=START_HOUR, minute=0)

class Sensor(models.Model):
    bar = models.ForeignKey(Bar, related_name="sensors")
    name = models.CharField(_("name"), max_length=100)
    volume = models.FloatField(_("volume"))
    bpm = models.FloatField(_("bpm"))
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s db - %s bpm" % (self.volume, self.bpm)

    def __unicode__(self):
        return str(self)

    class Meta:
        ordering = ['-created_at']

class CheckIn(models.Model):
    isMale = models.BooleanField(_("is gender male?"), default=False)
    age = models.IntegerField(_("age"))
    bar = models.ForeignKey(Bar, related_name="checkins")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s %d" % (self.bar.name, "Male" if self.isMale else "Female", self.age)
        
    def __unicode__(self):
        return str(self)

    class Meta:
        ordering = ['-created_at']

class Bouncer(models.Model):
    """Links a user to a bar and has a 1-1 relationship with Beaglebone devices"""
    user = models.ForeignKey(User, related_name="bouncer")
    bar = models.ForeignKey(Bar, related_name="bouncer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
        
    def __unicode__(self):
        return str(self)
