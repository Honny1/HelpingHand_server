import argparse

import requests

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--ip", action="store", help="store ip")
parser.add_argument("--state", action="store")
options = parser.parse_args()

state = "Off"
if options.state=="True":
    state = "On"
ip="http://" + options.ip + "/" + state
requests.get(ip)

