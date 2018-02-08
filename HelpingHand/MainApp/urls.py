from django.conf.urls import url

from MainApp import views

# IP/


urlpatterns = [
    url(r'login', views.login, name="login"),
    url(r'register', views.register, name="register"),
    url(r'logout', views.logout, name="logout"),
    url(r'config', views.config, name="config"),
    url(r'', views.index, name="index"),
]
