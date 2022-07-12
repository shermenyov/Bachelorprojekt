### Beschreibung des Backends Test für die Authentifizierung und Datensammlung
- Beide Geräte sind durch PoE Anschlüsse mit einem Switch verbunden
- Die IP Adressen der Geräte sind gegeben: 192.168.11.35 und 192.168.11.36
- Die IPs von Geräten und Einloggendaten müssen in die Datei deviceInfo.json übertragen werden, da die weiter im Skript abgefragt werden
- Alle Geräte müssen angeschlossen werden, ansonsten erscheint eine Error-Meldung

#### Folgende Packages müssen vorinstalliert sein:
- python
- pip
- npm (im Verzeichnis .../Vue)

#### Verzeichnis Flask
- im Terminal `cd .../Flask` - das Verzeichnis erreichen 
- weiter im Terminal `python app.py` -  Server-Backend mit einem default Port 5000 starten
- im Browser `http://localhost:5000/devices` - gibt die Daten der gewünschten Daten der Geräte zurück

#### Server-Backend als Dockercontainer starten
- im Terminal `cd .../Flask` und dann `docker build -t python-docker .` - Installation vom Image 'python-docker' 
- `docker run -p 5000:5000 -d python-docker` - Server startet als Container und ist im Browser erreichbar mit `http://localhost:5000/devices`

#### Verzeichnis Vue
- im Terminal `cd .../Vue` - das Verzeichnis erreichen 
- weiter im Terminal `npm run serve` - Server-Frontend der Link der Server-Webseite wird im Terminal übergeben (standartmäßig: <lokale IP Adresse>:8080) 
-  im Browser `http://<lokale IP Adresse>:8080` - Aufruf von der Server-Webseite

#### Server-Frontend als Dockercontainer starten
- im Terminal `cd .../Vue` und dann `docker build -t vue-docker .` - Installation vom Image 'python-docker' 
- `docker run -it -p 8080:8080 -d vue-docker` - Server startet als Container und ist im Browser erreichbar mit `http://<lokale IP Adresse>:8080`

#### Bemerkungen
- Es fehlt noch die Implementierung vom Datenbank auf dem Backend, um die Gerätegeschichte zu speichern
- Ein Fehler wurde während dem Testen herausgefunden, dass wenn man ein oder mehrere laufende Geräte auf der Webseite löscht, dann wird die JSON Datei mit Gerätedaten komischeweise komplett gelöscht. Das schaue ich noch genauer, damit das nicht mehr passiert.
