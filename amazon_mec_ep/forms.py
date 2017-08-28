from django import forms
from .models import AmazonMecEpSeries


BLANK = (("", "N/A"),)

PROVIDERS = (("E1", "Entertainment One"),
             ("utmw", "Under the Milky Way"),)

LANGUAGES = (("en", "English"),
             ("fr", "French"),)

REGIONS = (("CA", "Canada"),
          ("US", "United States of America"),)

GENRES = (("av_genre_action", "Action"),
          ("av_genre_comedy", "Comedy"),)


# class AmazonMecEpForm(forms.Form):
#     provider = forms.ChoiceField(
#         choices=PROVIDERS, )
#     original_language_locale = forms.ChoiceField(
#         choices=LANGUAGES, )
#     original_language_region = forms.ChoiceField(
#         choices=REGIONS, )
#     genre1 = forms.ChoiceField(
#         choices=GENRES, )
#     genre2 = forms.ChoiceField(
#         choices=BLANK + GENRES,
#         required=False)
#     genre3 = forms.ChoiceField(
#         choices=BLANK + GENRES,
#         required=False)

class AmazonMecEpSeriesForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
