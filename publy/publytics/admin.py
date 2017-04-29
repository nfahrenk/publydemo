from django.contrib import admin
from publytics.models import CheckIn, Bar, Bouncer, Sensor

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    fields = ('isMale', 'age', 'created_at', 'bar')

@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    fields = ('name', 'zipcode')

@admin.register(Bouncer)
class BouncerAdmin(admin.ModelAdmin):
    fields = ('user', 'bar')

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    fields = ('volume', 'bpm', 'created_at', 'bar')