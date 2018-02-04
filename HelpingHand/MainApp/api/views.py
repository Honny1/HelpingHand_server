import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from requests import session
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from MainApp.api.serializers import UserSerializer
from MainApp.models import User

class Login(APIView):
    def post(self,request):
        password=request.get("password",None)
        username=request.get("username",None)
        if password and username:
            user=User.objects.filter(username=username,password=password)
            if user:
                serializer = UserSerializer(user)
                return JSONRenderer().render(serializer.data)
        return JSONRenderer().render("{test}")

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class ListUsers(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


def turnLight(request):
    os.system("python3 /home/mnecas/Desktop/Projects/HelpingHand/HelpingHand_server/socket_server/client.py")
    return HttpResponse("test")