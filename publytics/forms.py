from django.forms import ModelForm, ValidationError
from publytics.models import CheckIn, Bar, Sensor

class CheckInForm(ModelForm):
    def clean_age(self):
        """Validate age to make sure that the person is at least 21 years old"""
        age = self.cleaned_data['age']
        if age < 21 or age > 130:
            raise ValidationError("Age must be between 21 and 130 inclusive.")
        return age

    def saveWithBar(self, bar, commit=True):
        checkin = CheckIn(
            isMale=self.cleaned_data['isMale'],
            age=self.cleaned_data['age'],
            bar=bar,
            created_at=Bar.now())
        if commit:
            checkin.save()
        return checkin

    class Meta:
        model = CheckIn
        fields = ["isMale", "age"]

class SensorForm(ModelForm):
    def saveWithBar(self, bar, commit=True):
        feed = Sensor(
            volume=self.cleaned_data['volume'],
            bpm=self.cleaned_data['bpm'],
            bar=bar,
            created_at=Bar.now())
        if commit:
            feed.save()
        return feed

    class Meta:
        model = Sensor
        fields = ["volume", "bpm"]