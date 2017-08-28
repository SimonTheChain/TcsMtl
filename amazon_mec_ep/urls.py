from django.conf.urls import url
from . import views


app_name = "amazon_mec_ep"

urlpatterns = [
    # metadata/amazon/mec/ep
    url(r'^$', views.index, name="index"),
]
