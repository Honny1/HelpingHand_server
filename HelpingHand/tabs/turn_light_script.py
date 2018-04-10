import argparse
import requests

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--ip", action="store", help="store ip")
parser.add_argument("--state", action="store")
parser.add_argument("--user", action="store")
options = parser.parse_args()
#Device.objects.filter(user=User.objects.filter(username=options.user).first(),ip=options.ip).update(state=options.state)

state = "Off"
if options.state=="True":
    state = "On"
ip="http://" + options.ip + "/" + state
requests.get(ip)
