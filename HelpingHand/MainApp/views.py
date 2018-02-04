from django.shortcuts import render, redirect

from .models import User


def index(request):
    if request.method == "GET":
        if not request.session.get("username", ""):
            return redirect("/login")

        return render(request, "index.html")


def login(request):
    if request.method == "GET":
        if not request.session.get("username", ""):
            return render(request, "login.html")
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if User.objects.filter(username=username, password=password):
            request.session["username"] = username
            return redirect("/index")
        return render(request, "login.html", {"error": "Bad username or password!"})


def logout(request):
    del request.session["username"]
    return redirect("/login")

def register(request):
    if request.method == "GET":
        if not request.session.get("username", ""):
            return render(request, "registration.html")
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password1", "")
        mail = request.POST.get("email", "")
        if "" in [username, mail, password]:
            return render(request, "registration.html", {"error": "Bad input!"})

        if User.objects.filter(username=username, mail=mail).exists():
            return render(request, "registration.html", {"error": "User already exists!"})

        request.session["username"] = username
        User(mail=mail, username=username, password=password).save()
        return redirect("/")
