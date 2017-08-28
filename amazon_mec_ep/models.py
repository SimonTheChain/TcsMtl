from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    amazon_code = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


class AmazonMecEpSeries(models.Model):
    name = models.CharField(max_length=100, unique=True)
    provider = models.ForeignKey(Provider)

    def __str__(self):
        return self.name


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
