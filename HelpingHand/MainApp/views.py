from copy import copy

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import User, Device, Configuration, Day


def index(request):
    if request.method == "GET":
        if not request.session.get("username", ""):
            return redirect("/login")

        return render(request, "index.html",
                      {"Devices":
                          Device.objects.filter(
                              user=User.objects.filter(username=request.session.get("username", ""))),
                          "Configs":
                              Configuration.objects.filter(device=Device.objects.filter(
                                  user=User.objects.filter(username=request.session.get("username", "")))),
                          "Days":
                              Day.objects.filter(
                                  configuration=Configuration.objects.filter(device=Device.objects.filter(
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
    if request.method == "POST":
        name = request.POST.get("device_name")
        request.session["device_name"] = name
    WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    name = request.session["device_name"]
    config = Configuration.objects.filter(
        device=Device.objects.filter(name=name,
                                     user=User.objects.filter(username=request.session.get("username", ""))))
    return render(request, "configs.html", {"Configs": config,
                                            "Days": WEEK})


def register(request):
    if request.method == "GET":
        if not request.session.get("username", ""):
            return render(request, "registration.html")
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password1", "")
        email = request.POST.get("email", "")
        if "" in [username, email, password]:
            return render(request, "registration.html", {"error": "Bad input!"})

        if User.objects.filter(username=username, email=email).exists():
            return render(request, "registration.html", {"error": "User already exists!"})
        open("tabs/" + username + ".tab", "w+")
        request.session["username"] = username
        User(email=email, username=username, password=password).save()
        return redirect("/")


def save_cron(username):
    from crontab import CronTab
    import os
    cron = CronTab(tabfile="tabs/" + username + '.tab', user=True)
    cron.remove_all()

    data = Configuration.objects.filter(
        device=Device.objects.filter(user=User.objects.filter(username=username).first()))
    WEEK = {"Monday": "MON", "Tuesday": "TUE", "Wednesday": "WED", "Thursday": "THU", "Friday": "FRI",
            "Saturday": "SAT",
            "Sunday": "SUN"}
    for config in data:
        hour = config.hours
        minutes = config.minutes
        state = config.state
        device_ip = config.device.ip
        job = cron.new(command='python3 /home/mnecas/Desktop/Projects/HelpingHand/HelpingHand_server/HelpingHand/tabs/turn_light_script.py --ip ' + device_ip + ' --state ' + str(state))
        week_day = []
        for day in Day.objects.filter(configuration=config):
            week_day.append(WEEK[day.name])
        if week_day:
            job.setall(minutes, hour, "*", "*", ",".join(week_day))
        else:
            job.setall(minutes, hour, "*", "*", "*")

    cron.write()
    os.system("crontab tabs/" + username + '.tab')


def save_data(request):
    if request.method == "GET":
        return HttpResponse("W")
    if request.method == "POST":
        ids = request.POST.getlist("ids[]")
        hours = request.POST.getlist("hours[]")
        minutes = request.POST.getlist("minutes[]")
        names = request.POST.getlist("config_names[]")
        cliecked = request.POST.getlist("states[]")

        def is_in_list(obj, list):
            for id in list:
                if id == obj:
                    return True
            return False

        states = []
        for id in copy(ids):
            if is_in_list(id, cliecked):
                states.append(True)
            else:
                states.append(False)

        for i in range(len(hours)):
            Configuration.objects.filter(
                id=ids[i]
            ).update(
                hours=hours[i],
                minutes=minutes[i],
                name=names[i],
                state=states[i])

        days = request.POST.getlist("days[]")
        for day_with_id in days:
            day_name = day_with_id.split("-")[0]
            config_id = day_with_id.split("-")[1]
            Day.objects.get_or_create(name=day_name, configuration=Configuration.objects.filter(id=config_id).first())
            for del_day in Day.objects.filter(configuration=Configuration.objects.filter(id=config_id).first()):
                if not is_in_list(del_day.name + "-" + config_id, days):
                    del_day.delete()

        save_cron(request.session.get("username", ""))
        return redirect("/")


def add_config(request):
    if request.method == "GET":
        Configuration(name="config",
                      device=Device.objects.filter(
                          name=request.session.get("device_name", ""),
                          user=User.objects.filter(username=request.session.get("username", "")).first(),
                      ).first()).save()
        return redirect("/config")


def delete_config(request):
    Configuration.objects.filter(id=request.POST.get("del_config", "")).delete()
    return redirect("/config")
