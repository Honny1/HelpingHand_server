from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from MainApp.api import views

# IP/api/
urlpatterns = [
    url('login', views.Login, name="login"),
    url('register', views.Register, name="Register"),
    url('lightInfo', views.LightInfo, name="LightInfo"),
    url('turnLight', views.turnLight, name="turnLight"),
    url('userInfo', views.UserInfo, name="UserInfo"),
    url('deviceSave', views.deviceSave, name="UserInfo"),
    url('configSave', views.configSave, name="UserInfo"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
