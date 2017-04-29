import django
django.setup()

from publytics.models import Bar, Sensor

bars = {
   'Ten Forward'             : (0.5, 63),
   'Taffey\'s Snake Pit Bar' : (0.55, 123),
   'Sister Louisa\'s Church' : (0.32, 200),
   'Mos Eisley Cantina'      : (0.8, 65),
   'Trees'                   : (0.34, 87),
   'new Bar'                 : (0.44, 106),
   'myBar'                   : (0.81, 96),
   'this.bar'                : (0.65, 123),
   'Foo Bar'                 : (0.32, 183),
   'Dada'                    : (0.87, 206)
}
for barName, info in bars.items():
   bar = Bar.objects.get(name=barName)
   feed = Sensor(
      volume=info[0],
      bpm=info[1],
      bar=bar,
      created_at=Bar.now())
   feed.save()