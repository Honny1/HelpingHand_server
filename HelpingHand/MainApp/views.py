from django.shortcuts import render, redirect

from .models import User, Device, Configuration, Day


def index(request):
    if request.method == "GET":
        if not request.session.get("username", ""):
            return redirect("/login")

        return render(request, "index.html",
                      {"Devices":
                           Device.objects.filter(user=User.objects.filter(username=request.session.get("username",""))),
                        "Configs":
                            Configuration.objects.filter(device=Device.objects.filter(user=User.objects.filter(username=request.session.get("username","")))),
                       "Days":
                           Day.objects.filter(configuration=Configuration.objects.filter(device=Device.objects.filter(
                               user=User.objects.filter(username=request.session.get("username", "")))))})


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

def config(request):
    name = request.POST.get("device_name")
    config=Configuration.objects.filter(device=Device.objects.filter(name=name,user=User.objects.filter(username=request.session.get("username",""))))
    print(config)
    print(Day.objects.filter(configuration=config))
    return render(request,"configs.html",{"Configs":config,
                                          "Selected_day":Day.objects.filter(configuration=config),
                                          "Days":["Monday","Tuesday","Wednesday","Thursday","Saturday","Sunday"]})

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

def save_data(request):
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass