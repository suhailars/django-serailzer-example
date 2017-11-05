from django.conf.urls import include, url
from .views import (
	LoginView,
	PageView,
	PageInfo,
)


urlpatterns = [
    url(r'^send_auth_token/$', LoginView.as_view()),
    url(r'^pages/$', PageView.as_view()),
    url(r'^pages/(?P<pk>[0-9]+)/$', PageInfo.as_view()),
]