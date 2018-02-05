from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^api', include("MainApp.api.urls")),
    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin', admin.site.urls),
    url(r'', include("MainApp.urls")),
]
