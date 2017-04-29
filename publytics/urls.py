from django.conf.urls import url
from publytics import views

app_name = 'publytics'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^checkin/$', views.CheckInList.as_view(), name='checkin'),
    url(r'^sensor/$', views.SensorList.as_view(), name='sensor'),
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^(?P<version>live|demo)/bar/(?P<pk>[0-9]+)/$', views.BarDetail.as_view(), name='bar'),
    url(r'^api/(?P<version>live|demo)/bars/(?P<zipcode>[0-9]{5})/$', views.BarList.as_view(), name='bars'),
    url(r'^api/(?P<version>live|demo)/gender/(?P<pk>[0-9]+)/$', views.RatioView.as_view(), name='gender'),
    url(r'^api/(?P<version>live|demo)/ages/(?P<pk>[0-9]+)/$', views.AgesView.as_view(), name='ages'),
    url(r'^api/(?P<version>live|demo)/activity/(?P<pk>[0-9]+)/$', views.TimeActivityView.as_view(), name='activity'),

]