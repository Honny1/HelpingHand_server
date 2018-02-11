import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json

from MainApp.api.serializers import UserSerializer
from MainApp.models import User, Device, Configuration, Day


@csrf_exempt
def Login(request):
    if request.method == "GET":
        return HttpResponse("error")
    if request.method == "POST":
        password = request.POST.get("password", "")
        username = request.POST.get("username", "")
        if password and username:
            user = User.objects.filter(username=username)
            if user.exists():
                serializer = UserSerializer(user.first())
                return HttpResponse(json.dumps(serializer.data))
            return HttpResponse("error")
        return HttpResponse("error")


@csrf_exempt
def Register(request):
    if request.method == "GET":
        return HttpResponse(json.dumps("error"))
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        email = request.POST.get("email", "")
        print(request.POST)
        if "" in [username, email, password]:
            return HttpResponse("error")

        if User.objects.filter(username=username, mail=email).exists():
            return HttpResponse(json.dumps({"error": "User already exists!"}))
        User(mail=email, username=username, password=password).save()
        return HttpResponse(json.dumps("SUCCES"))


@csrf_exempt
def LightInfo(request):
    if request.method == "GET":
        return HttpResponse("error")
    if request.method == "POST":
        device_info = json.loads(request.body.decode("utf-8"))
        try:
            Device.objects.get_or_create(ip=device_info["ip"],
                                         user=User.objects.filter(username=device_info["username"]).first())
        except Exception as exp:
            print(exp)
        return HttpResponse("done")


@csrf_exempt
def UserInfo(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return HttpResponse(json.dumps(serializer.data))
    if request.method == "POST":
        try:
            user = User.objects.filter(username=request.POST.get("username", "")).first()
            user_serializer = UserSerializer(user)
            return HttpResponse(json.dumps(user_serializer.data))
        except Exception as exp:
            print(exp)
            return HttpResponse("error")


def turnLight(request):
    os.system("python3 /home/mnecas/Desktop/Projects/HelpingHand/HelpingHand_server/socket_server/client.py")
    return HttpResponse("test")


@csrf_exempt
def deviceSave(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        device_id = request.POST.get("device_id", "")
        device_name = request.POST.get("light_name", "")
        Device.objects.filter(id=device_id).update(name=device_name)
        return HttpResponse("success")


@csrf_exempt
def delete_config(request):
    Configuration.objects.filter(id=int(request.POST.get("config_id", ""))).delete()
    return HttpResponse("done")


@csrf_exempt
def add_config(request):
    if request.method == "POST":
        Configuration(name="config",
                      device=Device.objects.filter(id=int(request.POST.get("device_id", ""))).first()).save()
        return HttpResponse("done")


@csrf_exempt
def configSave(request):
    if request.method == "POST":

        def is_in_list(obj, list):
            for id in list:
                if id == obj:
                    return True
            return False

        days_name = {"0": "Monday",
                     "1": "Tuesday",
                     "2": "Wednesday",
                     "3": "Thursday",
                     "4": "Friday",
                     "5": "Saturday",
                     "6": "Sunday"}
        days = {}
        shorter_list = []
        for i in range(7):
            if request.POST.get(days_name[str(i)], "") == "true":
                days[str(i)] = True
                shorter_list.append(days_name[str(i)])
            else:
                days[str(i)] = False

        state = request.POST.get("state", "")
        config_name = request.POST.get("config_name", "")
        hours = request.POST.get("hours", "")
        minutes = request.POST.get("minutes", "")
        username = request.POST.get("username", "")
        device_name = request.POST.get("device_name", "")
        device_id = request.POST.get("device_id", "")
        config_id = request.POST.get("config_id", "")
        config = Configuration.objects.filter(id=int(config_id),
                                              device=Device.objects.filter(id=int(device_id)).first())
        bol_state = False
        if state == "true":
            bol_state = True

        config.update(hours=hours, minutes=minutes, name=config_name, state=bol_state)
        for key, value in days.items():
            if value:
                Day.objects.get_or_create(name=days_name[key], configuration=config.first())

        for del_day in Day.objects.filter(configuration=config):
            if not is_in_list(del_day.name, shorter_list):
                del_day.delete()

        return HttpResponse("success")
