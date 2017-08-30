from django import forms
from .models import Series


class SeriesForm(forms.ModelForm):

    class Meta:
        model = Series
        fields = [
            "name",
            "original_language_locale",
            "original_language_region",
            "genre1",
            "genre2",
            "genre3",
            "provider"
        ]
