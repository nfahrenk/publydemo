from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from publytics.models import Bar, Bouncer
from django.shortcuts import get_object_or_404
from publytics.forms import CheckInForm, SensorForm
from django.db import models
from datetime import timedelta
from myglobals import AGE_RANGES, MINS_PER_CHUNK, START_HOUR
from django.shortcuts import render

def generateDemoTime(version, params):    
    if version == 'demo':
        try:
            return Bar.generateDemoTime(
                int(params.get("hours", START_HOUR)), 
                int(params.get("mins", 0)))
        except ValueError:
            return Bar.generateDemoTime(START_HOUR, 0)
    else:
        return None

class CalendarView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return render(request, 'calendar.html', {})

class IndexView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return render(request, 'index.html', {
            "zipcode": request.GET.get("zipcode"),
            "hours": request.GET.get("hours"),
            "mins": request.GET.get("mins")            
            })

class CheckInList(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = CheckInForm(request.POST)

        if form.is_valid():
            try:
                form.saveWithBar(Bouncer.objects.get(user=request.user).bar, commit=True)
                return JsonResponse({"response": "ok"})
            except Bouncer.DoesNotExist:
                return JsonResponse({"errors": form.errors}, status=400)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

class SensorList(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = SensorForm(request.POST)

        if form.is_valid():
            try:
                form.saveWithBar(Bouncer.objects.get(user=request.user).bar, commit=True)
                return JsonResponse({"response": "ok"})
            except Bouncer.DoesNotExist:
                return JsonResponse({"errors": "form.errors"}, status=400)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

class BarDetail(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, version, pk):
        time = generateDemoTime(version, request.GET)
        bar = get_object_or_404(Bar, pk=pk)

        info = Bar.getAudioInfoByZipcode(bar.zipcode)

        return render(request, 'generic.html', {
            "name": bar.name,
            "hotness": bar.getRank(time),
            "volume": bar.getVolumeRank(info),
            "bpm": bar.getBpmRank(info),
            "barId": bar.pk,
            "zipcode": bar.zipcode,
            "hours": int(request.GET.get("hours", START_HOUR)),
            "mins": int(request.GET.get("mins", 0))
            })

class BarList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, version, zipcode):
        time = generateDemoTime(version, request.GET)

        sorted_bars = Bar.objects.filter(
            zipcode=zipcode) \
            .annotate(num_checkins=models.Sum(
                models.Case(
                    models.When(
                        checkins__created_at__gte=Bar.getTimeAnHourAgo(time), 
                        checkins__created_at__lte=Bar.getUpperTime(time), 
                        then=1),
                    default=0,
                    output_field=models.IntegerField()
                ))) \
            .order_by('-num_checkins')
        
        info = Bar.getInfoByZipcode(zipcode, time)

        return JsonResponse({
            "results": [
                {
                    "id": bar.pk,
                    "name": bar.name,
                    "hotness": bar.getRank(time, info, bar.num_checkins)
                }
                for bar in sorted_bars
            ]
            })

class RatioView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, version, pk):
        time = generateDemoTime(version, request.GET)
        bar = get_object_or_404(Bar, pk=pk)
        if Bar.now(time) >= Bar.getOpeningTime(time):
            return JsonResponse({
                "female": bar.getTodaysByGender(False, time),
                "male": bar.getTodaysByGender(True, time)
                })
        else:
            return JsonResponse({"errors": {"now": "Tonight's data is not yet available."}}, status=400)

class AgesView(APIView):
    authentication_classes = []
    permission_classes = []
    

    def get(self, request, version, pk):
        time = generateDemoTime(version, request.GET)
        bar = get_object_or_404(Bar, pk=pk)
        if Bar.now(time) >= Bar.getOpeningTime(time is not None):
            return JsonResponse({
                "results": [
                    {
                        "label": "%d - %d" % (val[0], val[1]),
                        "x": count,
                        "y": bar.getTodaysByAge(val[0], val[1], time)
                    }
                    for count, val in enumerate(AGE_RANGES)
                ]
                })
        else:
            return JsonResponse({"errors": {"now": "Tonight's data is not yet available."}}, status=400)

class TimeActivityView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, version, pk):
        time = generateDemoTime(version, request.GET)
        bar = get_object_or_404(Bar, pk=pk)
        opening = Bar.getOpeningTime(time is not None)
        closing = Bar.getUpperTime(time)
        if Bar.now(time) >= opening:
            results = []
            for count in range(0, ((closing-opening).seconds/60)/MINS_PER_CHUNK):
                startTime = opening + timedelta(minutes=MINS_PER_CHUNK*count)
                endTime = startTime + timedelta(minutes=MINS_PER_CHUNK)
                # Only add if that time is valid
                results.append({
                    "label": "%s - %s" % (startTime.strftime("%I:%M %p"), endTime.strftime("%I:%M %p")),
                    "x": count,
                    "y": bar.getTodaysTimeActivity(startTime, endTime)
                })
            return JsonResponse({"results": results})
        else:
            return JsonResponse({"errors": {"now": "Tonight's data is not yet available."}}, status=400)
