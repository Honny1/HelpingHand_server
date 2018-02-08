from django.conf.urls import url

from MainApp import views

# IP/


urlpatterns = [
    url(r'login', views.login, name="login"),
    url(r'register', views.register, name="register"),
    url(r'logout', views.logout, name="logout"),
    url(r'config', views.config, name="config"),
    url(r'add', views.add_config, name="add_config"),
    url(r'save_data', views.save_data, name="save_data"),
    url(r'delete', views.delete_config, name="delete_config"),
    url(r'', views.index, name="index"),
]
