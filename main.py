#!/usr/local/bin/python3

import yaml
import croniter
import datetime
import time
from importlib import import_module
import os


def importProvider(src: str):
    if not os.path.exists("providers/" + src + ".py"):
        return None
    return import_module("providers." + src)


def backup(providers, devices, git):
    basePath = git["folder"]
    for i in devices:
        if i["enabled"]:
            print("saving file: " + i["file"])
            try:
                providers[i["type"]].backup(
                    address=i["address"],
                    user=(i.get("user") or ""),
                    password=(i.get("password") or ""),
                    file=os.path.join(basePath, i["file"]),
                )
            except Exception as e:
                print("failed with error:", e)

    commitMessage = "Backup - " + datetime.datetime.now().strftime("%Y-%m-%d")
    print("pushing backup with message: " + commitMessage)
    os.system(
        "cd "
        + basePath
        + " && git pull "
        + git["repo"]
        + " && git add ."
        + " && git commit -m '"
        + commitMessage
        + "' && git push "
        + git["repo"]
        + " "
        + git["branch"]
    )


with open("config.yml") as f:
    config = yaml.full_load(f)
    print("Configuration loaded")

providers = {}
for i in config["devices"]:
    if i["type"] not in providers:
        providers[i["type"]] = importProvider(i["type"])
print("loaded", len(providers), "providers")

if not os.path.exists(config["git"]["folder"]):
    os.system("git clone " + config["git"]["repo"] + " " + config["git"]["folder"])
os.system(
    "cd " + config["git"]["folder"] + "&& git checkout " + config["git"]["branch"]
)

cron = None
if config["settings"]["cron"] != "":
    cron = croniter.croniter(config["settings"]["cron"], datetime.datetime.now())
while True:
    # start a backup
    backup(providers, config["devices"], config["git"])
    if cron is None:
        break
    # sleep until next occurrence
    nxt = cron.get_next(datetime.datetime)
    print("Next backup:", nxt)
    sleepTime = (nxt - datetime.datetime.now()).total_seconds()
    time.sleep(sleepTime)
