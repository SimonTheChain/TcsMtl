from django import forms
from .models import AmazonMecEpSeries


class AmazonMecEpSeriesForm(forms.ModelForm):

    class Meta:
        model = AmazonMecEpSeries
        fields = "__all__"
