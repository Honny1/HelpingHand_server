from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30, default="")
    password = models.CharField(max_length=300, default="")
    email = models.EmailField(default="")

    def right_user(self, username, password):
        if username == self.username and self.password == password:
            return True
        return False

    def is_registred(self, username):
        if username == self.username:
            return True
        return False

    def __str__(self):
        return str(self.username)


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device')
    name = models.CharField(max_length=100,default="device")
    state = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(default="127.0.0.1")

    def __str__(self):
        return str(self.user) + " - " + str(self.name)


class Configuration(models.Model):
    hours = models.IntegerField(default=0, null=True, blank=True)
    minutes = models.IntegerField(default=0, null=True, blank=True)
    name = models.CharField(max_length=100, default="")
    state = models.BooleanField(default=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='configuration', null=True)

    def get_days(self):
        days = Day.objects.filter(configuration=self)
        name_days = []
        for day in days:
            name_days.append(day.name)
        return name_days

    def __unicode__(self):
        return str(self.name) + " - " + str(self.hours) + "/" + str(self.minutes) + " - " + str(self.state)

    def __str__(self):
        return str(self.hours) + "/" + str(self.minutes) + " " + str(self.state)


class Day(models.Model):
    DAYS = (
        ("1", "Monday"), ("2", "Tuesday"), ("3", "Wednesday"), ("4", "Thursday"), ("5", "Friday"), ("6", "Saturday"),
        ("7", "Sunday"))
    name = models.CharField(choices=DAYS, max_length=20, default="Monday")
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE, related_name='day')

    def __str__(self):
        return str(self.name) + " " + str(self.configuration)
