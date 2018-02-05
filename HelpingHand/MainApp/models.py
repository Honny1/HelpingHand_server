from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=300)
    mail = models.EmailField(default="")

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


class Configuration(models.Model):
    time = models.TimeField()


class Device(models.Model):
    name = models.CharField(max_length=100)
    config = models.ForeignKey(Configuration,on_delete=models.CASCADE)
    state = models.CharField(max_length=50)