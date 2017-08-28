from django.shortcuts import render
from .forms import AmazonMecEpSeriesForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Provider, AmazonMecEpSeries, AmazonMecEpSeason, AmazonMecEpEpisode


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AmazonMecEpSeriesForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            provider = form.cleaned_data["provider"]
            language = form.cleaned_data["original_language_locale"]
            region = form.cleaned_data["original_language_region"]
            genre1 = form.cleaned_data["genre1"]
            genre2 = form.cleaned_data["genre2"]
            genre3 = form.cleaned_data["genre3"]

            return render(
                request,
                "amazon_mec_ep/index.html",
                context={
                    'form': form,
                    "provider": provider,
                    "language": language,
                    "region": region,
                    "genre1": genre1,
                    "genre2": genre2,
                    "genre3": genre3,
                }
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AmazonMecEpSeriesForm()

    return render(
        request,
        "amazon_mec_ep/index.html",
        context={'form': form})


class ProviderListView(ListView):
    model = Provider


class ProviderDetailView(DetailView):
    model = Provider

    def get_context_data(self, **kwargs):
        context = super(ProviderDetailView, self).get_context_data(**kwargs)
        return context


class ProviderCreate(CreateView):
    model = Provider
    fields = "__all__"


class ProviderUpdate(UpdateView):
    model = Provider
    fields = "__all__"
