from django.contrib import admin
from.models import Provider, AmazonMecEpSeries, AmazonMecEpSeason, AmazonMecEpEpisode


admin.site.register(Provider)
admin.site.register(AmazonMecEpSeries)
admin.site.register(AmazonMecEpSeason)
admin.site.register(AmazonMecEpEpisode)
