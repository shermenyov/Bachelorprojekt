from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests, json, time
from requests.structures import CaseInsensitiveDict

# Erstellen des Flask Instances
app = Flask(__name__)

# Keine Sortierung nach der Funktion jsonify()
app.config['JSON_SORT_KEYS'] = False

# Initialisierung von CORS (Cross Origin Resource Sharing)
CORS(app, support_credentials=True)

# Definierung der Daten von deviceInfo.json
with open("deviceInfo.json") as jsonFile:
   jsonObject = json.load(jsonFile)
   jsonFile.close()
ipaddHost = jsonObject["host"]
devConfigAPI = jsonObject["devicesConfigAPI"]
devLoginAPI = jsonObject["devicesLoginAPI"]
devTimeAPI = jsonObject["devicesTimeAPI"]

# Sammlung der laufenden und ausgeschalteten Geräten

devicesStatus = []
def updateStatus():
   # devicesStatus = []
   for index, device in enumerate(jsonObject["devices"]):
      try:
         devRes = requests.get(device["address"], timeout=3)
         if devRes.status_code == 200:
            devicesStatus.append(True)
         else:
            devicesStatus.append(False)
            pass
      except requests.exceptions.RequestException:
         devicesStatus.append(False)
updateStatus()

# Sammlung der Tokens für jedes Gerät
with open("deviceInfo.json", "w") as jsonFile:
   for index, device in enumerate(jsonObject["devices"]):
      if devicesStatus[index] == True:
         payload = {'username': device["username"], 'password': device["password"]}
         res = requests.post(device["address"] + devLoginAPI, json=payload)
         token = res.json()
         jsonObject["devices"][index]["token"] = token["token"]
   json.dump(jsonObject, jsonFile)
   jsonFile.close()

# Definierung der REST-API für den Empfang der bestimmten Daten für die Server-Anzeige
@app.route('/devices', methods = ['GET', 'POST'])
def get_devices():
   Data = []
   if request.method == 'GET':
      try:
         for index, device in enumerate(jsonObject["devices"]):
            if devicesStatus[index] == True:
               # Datensammlung von jedem Gerät nach dem Einloggen
               url_config = device["address"] + devConfigAPI
               headers = CaseInsensitiveDict()
               headers["Authorization"] = "Bearer " + device["token"]
               headers["Content-Type"] = "application/json; charset=utf-8"
               resp_config = requests.get(url_config, headers=headers)
               deviceValues = resp_config.json()

               url_time = device["address"] + devTimeAPI
               headers = CaseInsensitiveDict()
               headers["Authorization"] = "Bearer " + device["token"]
               headers["Content-Type"] = "application/json; charset=utf-8"
               resp_time = requests.get(url_time, headers=headers)
               deviceTime = resp_time.json()
               runtime = time.strftime('%H:%M:%S', time.gmtime(deviceTime["uptime"]))

               deviceData = {
                  "address": device["address"],
                  "id": index,
                  "boardTemperature": deviceValues["status"]["boardTemperature"],
                  "softwareVersion": deviceValues["status"]["softwareVersion"],
                  "speakerVolume": deviceValues["audioconfig"]["dynamic"][0]["speakerVolume"],
                  "microphoneVolume": deviceValues["audioconfig"]["dynamic"][0]["microphoneVolume"],
                  "ringToneVolume": deviceValues["audioconfig"]["dynamic"][0]["ringToneVolume"],
                  "signalToneVolume": deviceValues["audioconfig"]["dynamic"][0]["signalToneVolume"],
                  "announcementVolume": deviceValues["audioconfig"]["dynamic"][2]["speakerVolume"],
                  "runtime": runtime,
                  "systemTime": deviceTime["systemTime"]
               }
               Data.append(deviceData)
            else:
               deviceData = {
                  "address": device["address"],
                  "id": index,
                  "boardTemperature": '0000',
                  "softwareVersion": '0000',
                  "speakerVolume": '0000',
                  "microphoneVolume": '0000',
                  "ringToneVolume": '0000',
                  "signalToneVolume": '0000',
                  "announcementVolume": '0000',
                  "runtime": '0000',
                  "systemTime": '0000',
               }
               Data.append(deviceData)
         return jsonify(Data)
      except Exception as error:
         print("Error occurred :: %s" % error)
         return ""

@app.route('/connect', methods = ['GET', 'POST'])
def connect_device():
   if request.method == 'POST':
      try:
         with open("deviceInfo.json", "w") as jsonFile:
            jsonObject["devices"].append(request.get_json())
            jsonObject["devices"][len(jsonObject["devices"]) - 1]["token"] = ""
            json.dump(jsonObject, jsonFile)
            jsonFile.close()
            updateStatus()
         return ""
      except Exception as error:
         print("Error occurred :: %s" % error)
         return ""

@app.route('/disconnect', methods = ['GET', 'POST'])
def disconnect_device():
   if request.method == 'POST':
      try:
         with open("deviceInfo.json", "w") as jsonFile:
            jsonObject["devices"].pop(request.get_json()["id"])
            json.dump(jsonObject, jsonFile)
            jsonFile.close()
            updateStatus()
         return ""
      except Exception as error:
         print("Error occurred :: %s" % error)
         return ""


#Aufruf der Datei __main__.py startet Server mit einem default Port 5000
#Parametren in Funktion run(): 'use_reloader=False, debug = True' lassen den interaktiven Debugger
#aktivieren, ohne dass der Code neu geladen wird.

if __name__ == '__main__':
   app.run(debug = True, host=ipaddHost)

