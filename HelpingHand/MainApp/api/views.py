import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from requests import session
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from MainApp.api.serializers import UserSerializer
from MainApp.models import User

@csrf_exempt
def Login(request):
    if request.method=="GET":
        return HttpResponse({"error":"WRONG METHOD"})
    if request.method=="POST":
        password = request.POST.get("password", "")
        username = request.POST.get("username", "")
        if password and username:
            user = User.objects.filter(username=username)
            if user.exists():
                serializer = UserSerializer(user.first())
                return HttpResponse(json.dumps(serializer.data))
            return HttpResponse(json.dumps({"error":"WRONG USER"}))
        return HttpResponse(json.dumps({"error":"WRONG INPUT"}))

@csrf_exempt
def Register(request):
    if request.method == "GET":
        return HttpResponse(json.dumps({"error":"WRONG METHOD"}))
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        email = request.POST.get("email", "")
        print(request.POST)
        if "" in [username, email, password]:
            return HttpResponse(json.dumps({"error": "WRONG INPUT"}))

        if User.objects.filter(username=username, mail=email).exists():
            return HttpResponse(json.dumps({"error": "User already exists!"}))
        User(mail=email, username=username, password=password).save()
        return HttpResponse(json.dumps("SUCCES"))


def turnLight(request):
    os.system("python3 /home/mnecas/Desktop/Projects/HelpingHand/HelpingHand_server/socket_server/client.py")
    return HttpResponse("test")
