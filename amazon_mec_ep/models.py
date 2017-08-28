from django.urls import reverse
from django.db import models


BLANK = (("", "N/A"),)

LANGUAGES = (("en", "English"),
             ("fr", "French"),)

REGIONS = (("CA", "Canada"),
          ("US", "United States of America"),)

GENRES = (("av_genre_action", "Action"),
          ("av_genre_comedy", "Comedy"),)


class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    amazon_code = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('provider-detail', kwargs={'pk': self.pk})


class AmazonMecEpSeries(models.Model):
    name = models.CharField(max_length=100, unique=True)
    original_language_locale = models.CharField(max_length=2, choices=BLANK + LANGUAGES, default=None)
    original_language_region = models.CharField(max_length=2, choices=BLANK + REGIONS, default=None)
    provider = models.ForeignKey(Provider)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('series-detail', kwargs={'pk': self.pk})


class AmazonMecEpSeason(models.Model):
    name = models.CharField(max_length=100, unique=True)
    series = models.ForeignKey(AmazonMecEpSeries)
    provider = models.ForeignKey(Provider)

    def __str__(self):
        return self.name


class AmazonMecEpEpisode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    series = models.ForeignKey(AmazonMecEpSeries)
    season = models.ForeignKey(AmazonMecEpSeason)
    provider = models.ForeignKey(Provider)

    def __str__(self):
        return self.name
