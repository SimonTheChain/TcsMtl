from django.urls import reverse
from django.db import models
from converter import convert


BLANK = (("", "---------"),)

LANGUAGES = convert.create_languages()

REGIONS = convert.create_countries()

GENRES = (("av_genre_action", "Action"),
          ("av_genre_comedy", "Comedy"),)


class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    amazon_code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('amazon_mec_ep:provider-detail', kwargs={'pk': self.pk})


class TestClass(models.Model):
    test_field = models.CharField(max_length=250, choices=LANGUAGES)


class Series(models.Model):
    name = models.CharField(max_length=100, unique=True)
    amazon_id = models.CharField(max_length=50, unique=True)
    date = models.CharField(max_length=10, blank=True, null=True, default=None)
    original_language_locale = models.CharField(max_length=2, choices=LANGUAGES, default=None)
    original_language_region = models.CharField(max_length=2, choices=REGIONS, default=None)
    genre1 = models.CharField(max_length=50, choices=BLANK + GENRES, default="av_genre_action")
    genre2 = models.CharField(max_length=50, choices=BLANK + GENRES, blank=True, null=True, default=None)
    genre3 = models.CharField(max_length=50, choices=BLANK + GENRES, blank=True, null=True, default=None)
    provider = models.ForeignKey(Provider)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('amazon_mec_ep:series-detail', kwargs={'pk': self.pk})


class SeriesRating(models.Model):
    country = models.CharField(max_length=2, choices=REGIONS, blank=True, null=True, default=None)
    system = models.CharField(max_length=50, blank=True, null=True, default=None)
    value = models.CharField(max_length=50, blank=True, null=True, default=None)
    series = models.ForeignKey(Series)

    def __str__(self):
        return self.system

    def get_absolute_url(self):
        return reverse('amazon_mec_ep:rating-detail', kwargs={'pk': self.pk})


class SeriesInfo(models.Model):
    language_locale = models.CharField(max_length=2, choices=LANGUAGES, blank=True, null=True, default=None)
    language_region = models.CharField(max_length=2, choices=REGIONS, blank=True, null=True, default=None)
    default = models.BooleanField(default=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    summary_short = models.CharField(max_length=400, blank=True, null=True)
    summary_long = models.CharField(max_length=4000, blank=True, null=True)
    series = models.ForeignKey(Series)

    def __str__(self):
        return "{}-{}".format(self.language_locale, self.language_region)

    def get_absolute_url(self):
        return reverse('amazon_mec_ep:info-detail', kwargs={'pk': self.pk})


class Season(models.Model):
    name = models.CharField(max_length=100, unique=True)
    series = models.ForeignKey(Series)
    provider = models.ForeignKey(Provider)

    def __str__(self):
        return self.name


class Episode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    series = models.ForeignKey(Series)
    season = models.ForeignKey(Season)
    provider = models.ForeignKey(Provider)

    def __str__(self):
        return self.name
