from django.conf.urls import include, url
from .views import (
	InvoiceList,
	InvoiceDetails,
)
#from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^$', InvoiceList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', InvoiceDetails.as_view()),
    #url(r'^(?P<pk>[0-9]+)/subcategories/$', SubCategoryList.as_view()),
]