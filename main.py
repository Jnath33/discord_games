import os
import shutil
import subprocess
import time
from shutil import copyfile
import json

with open("settings/settings.json", "r") as f_settings:
    settings = json.load(f_settings)

subs_process = []

id_max = 0

for setting in settings["settings"]:
    id_max = max(int(setting["id"]), id_max)

for setting in settings["settings"]:
    if setting["id"] == "0":
        copyfile("settings/sous_bot.py", "bot" + setting["id"] + ".py")
        os.makedirs("bot" + setting["id"] + "/data")
        subs_process.append(subprocess.Popen(["python3",
                                              "bot" + setting["id"] + ".py",
                                              json.dumps(setting, separators=(',', ':'))]))
        copyfile("settings/main_bot.py", "main-bot.py")
        subs_process.append(subprocess.Popen(["python3",
                                              "main-bot.py",
                                              json.dumps(setting, separators=(',', ':')),
                                              str(id_max)]))
    else:
        copyfile("settings/sous_bot.py", "bot" + setting["id"] + ".py")
        os.makedirs("bot" + setting["id"] + "/data")
        subs_process.append(subprocess.Popen(["python3",
                                              "bot" + setting["id"] + ".py",
                                              json.dumps(setting, separators=(',', ':'))]))

time.sleep(10)
a = ""
while a != "y":
    a = input("stop ? (y) : ")

for sub in subs_process:
    sub.kill()

for f in next(os.walk("./"), (None, None, []))[2]:
    if "bot" in f:
        os.remove(f)
for setting in settings["settings"]:
    shutil.rmtree("bot" + setting["id"])
