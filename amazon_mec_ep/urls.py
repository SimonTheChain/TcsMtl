from django.conf.urls import url
from .views import \
    ProviderListView, \
    ProviderDetailView, \
    ProviderCreate, \
    ProviderUpdate, \
    ProviderDelete, \
    SeriesList, \
    SeriesCreate, \
    SeriesDetail, \
    SeriesUpdate, \
    SeriesDelete, \
    SeriesRatingCreate, \
    SeriesRatingDetail, \
    SeriesRatingUpdate, \
    SeriesRatingDelete, \
    SeriesInfoCreate, \
    SeriesInfoDetail, \
    SeriesInfoUpdate, \
    SeriesInfoDelete, \
    mec_series, \
    mec_missing, \
    ingest


app_name = "amazon_mec_ep"

urlpatterns = [
    # metadata/
    # url(r'^$', index, name="index"),

    # ingest/
    url(r'ingest/$', ingest, name='ingest'),

    # provider/
    url(r'provider/list/$', ProviderListView.as_view(), name='provider-list'),
    url(r'provider/(?P<pk>[0-9]+)/$', ProviderDetailView.as_view(), name='provider-detail'),
    url(r'provider/add/$', ProviderCreate.as_view(), name='provider-add'),
    url(r'provider/(?P<pk>[0-9]+)/edit/$', ProviderUpdate.as_view(), name='provider-update'),
    url(r'provider/(?P<pk>[0-9]+)/delete/$', ProviderDelete.as_view(), name='provider-delete'),

    # series/
    url(r'series/list/$', SeriesList.as_view(), name='series-list'),
    url(r'series/add/$', SeriesCreate.as_view(), name='series-add'),
    url(r'series/(?P<pk>[0-9]+)/$', SeriesDetail.as_view(), name='series-detail'),
    url(r'series/edit/(?P<pk>[0-9]+)/$', SeriesUpdate.as_view(), name='series-update'),
    url(r'series/(?P<pk>[0-9]+)/delete/$', SeriesDelete.as_view(), name='series-delete'),
    url(r'series/mec/(?P<pk>[0-9]+)/$', mec_series, name='series-mec'),
    url(r'series/mec/(?P<pk>[0-9]+)/missing/$', mec_missing, name='series-mec-missing'),

    # series localized info
    url(r'series/rating/add/$', SeriesRatingCreate.as_view(), name='rating-add'),
    url(r'series/rating/(?P<pk>[0-9]+)/$', SeriesRatingDetail.as_view(), name='rating-detail'),
    url(r'series/rating/edit/(?P<pk>[0-9]+)/$', SeriesRatingUpdate.as_view(), name='rating-update'),
    url(r'series/rating/(?P<pk>[0-9]+)/delete/$', SeriesRatingDelete.as_view(), name='rating-delete'),

    # series localized info
    url(r'series/info/add/$', SeriesInfoCreate.as_view(), name='info-add'),
    url(r'series/info/(?P<pk>[0-9]+)/$', SeriesInfoDetail.as_view(), name='info-detail'),
    url(r'series/info/edit/(?P<pk>[0-9]+)/$', SeriesInfoUpdate.as_view(), name='info-update'),
    url(r'series/info/(?P<pk>[0-9]+)/delete/$', SeriesInfoDelete.as_view(), name='info-delete'),
]
