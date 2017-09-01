from django.contrib import admin
from.models import TestClass, Provider, Series, SeriesRating, SeriesInfo, Season, Episode


admin.site.register(Provider)
admin.site.register(Series)
admin.site.register(SeriesRating)
admin.site.register(SeriesInfo)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(TestClass)