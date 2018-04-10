from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from MainApp.api import views

# IP/api/
urlpatterns = [
    url('login', views.Login, name="login"),
    url('register', views.Register, name="Register"),
    url('lightInfo', views.LightInfo, name="LightInfo"),
    url('userInfo', views.UserInfo, name="UserInfo"),
    url('deviceSave', views.deviceSave, name="UserInfo"),
    url('configSave', views.configSave, name="UserInfo"),
    url('addConfig', views.add_config, name="add_config"),
    url('delConfig', views.delete_config, name="delConfig"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
