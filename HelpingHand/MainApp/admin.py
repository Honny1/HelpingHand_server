from django.contrib import admin

from .models import User, Configuration, Device, Day

# Register your models here.

admin.site.register(User)
admin.site.register(Configuration)
admin.site.register(Device)
admin.site.register(Day)
