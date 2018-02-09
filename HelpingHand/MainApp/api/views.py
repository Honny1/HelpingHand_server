import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json

from MainApp.api.serializers import UserSerializer
from MainApp.models import User, Device, Configuration


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
        device_id= request.POST.get("device_id","")
        device_name= request.POST.get("light_name","")
        Device.objects.filter(id=device_id).update(name=device_name)
        return HttpResponse("succes")


@csrf_exempt
def configSave(request):
    if request.method == "POST":
        print(request.POST)
        days = []
        for i in range(7):
            days.append(request.POST.get("checkBoxes" + str(i), ""))
        state = request.POST.get("state", "")
        config_name = request.POST.get("config_name", "")
        hours = request.POST.get("hours", "")
        minutes = request.POST.get("minutes", "")
        username = request.POST.get("username", "")
        device_name = request.POST.get("device_name", "")
        device_id = request.POST.get("device_id", "")
        config_id = request.POST.get("config_id", "")
        Configuration.objects.filter(id=int(config_id),
            device=Device.objects.filter(id=int(device_id)).first()).update(hours=hours,minutes=minutes,name=config_name,state=state)
        return HttpResponse("succes")

