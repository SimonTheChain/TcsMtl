from django.conf.urls import url
from .views import ProviderListView, ProviderDetailView, ProviderCreate, ProviderUpdate


app_name = "amazon_mec_ep"

urlpatterns = [
    # metadata/amazon/mec/episodic
    # url(r'^$', views.index, name="index"),
    url(r'^$', ProviderListView.as_view(), name='provider-list'),
    url(r'provider/(?P<pk>[0-9]+)/$', ProviderDetailView.as_view(), name='provider-detail'),
    url(r'provider/add/$', ProviderCreate.as_view(), name='provider-add'),
    url(r'provider/update/(?P<pk>[0-9]+)/$', ProviderUpdate.as_view(), name='provider-update'),

]
