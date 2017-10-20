from django.conf.urls import include, url
from .views import (
	InvoiceList,
	InvoiceDetails,
)


urlpatterns = [
    url(r'^$', InvoiceList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', InvoiceDetails.as_view()),
]