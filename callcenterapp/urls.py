from django.conf.urls import url

from callcenterapp import views

urlpatterns = [
    url(r'^calls/$', views.CallCenterService.as_view(), name='call-list'),
    url(r'^config/$', views.JiraConfiguration.as_view(), name='config-list'),
]
