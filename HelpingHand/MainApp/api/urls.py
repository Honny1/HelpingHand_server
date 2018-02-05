from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from MainApp.api import views

#IP/api/
urlpatterns = [
    url('login', views.Login, name="login"),
    url('register', views.Register, name="login"),
    url('turnLight', views.turnLight, name="login"),
]
urlpatterns=format_suffix_patterns(urlpatterns)
