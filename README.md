# RESTful Web Services SS 2023

Luca Bauernfeind, Leon Frenzl, Philipp Glaser, Gregory Mehlhorn, Rouven Weil

## Thema
Die Gruppe erstellt einen Webservice zur Verbindung von Twitter und Spotify. Die API kann aus einer Liste, welche aus Interpreten, Genres, Alben oder Songs bestehen kann, einen Post generieren. 

Auch gibt es die Möglichkeit eine Playlist von Spotify zu einer Deezer Playlist zu konvertieren.

## Anwendung starten

### Backend API starten
`pip install -r requirements.txt`

`cd /app/`

`uvicorn main:app --reload`

### Frontend starten
`cd /client/`

`npm install`

`npm run dev`

## Problem mit .env

Unter normalen Umständen wäre es nicht üblich, eine .env Datei im Repository zu verwalten, aber aus Gründen der akademischen Zugänglichkeit haben wir uns dagegen entschieden. 

## Beschreibung der Idee
[Präsentationsfolien](Projektvorstellung_mit_API-Endpunkten.pdf)

## Beschreibung der Schnittstelle
[Ursprüngliche yaml-Version](openapi_1.yaml)

Aktuelle HTMl-Version: `http://localhost:8000/docs`

## Beschreibung der genutzten APIs und deren Konfigurationsmöglichkeiten

### Spotify
Die Spotify API wurde über die Standard Web API angebunden. Spotify wird verwendet um Playlists zu laden, aus welchen ein Bild generiert werden kann. Hierfür wurde bei der Spotify Web Api eine App erstellt, welche die Daten zu Authentifizierung notwendig sind. 

Hier mussten auser eine Domain aber sonst keine besonderen Dinge gesetzt werden.

### Deezer
Die Deezer API wurde über die Standard Deezer API angebunden. Diese kann allerdings nur verwendet werden, wenn man bereits ein Deezer Konto besitzt. Dieses Kostet 10€ im Monat. Deezer wird verwendet um Playlists von Spotify zu Deezer und andersherum convertieren. Hierfür wurde bei der Deezer Api eine App erstellt, welche die Daten zu Authentifizierung notwendig sind. 

Hier mussten auser eine Domain aber sonst keine besonderen Dinge gesetzt werden.

### Twitter
Für das Projekt wurde sowohl Standard v1.1 sowie Twitter API v2 genutzt. Die Anbindung wird verwendet, um aus unseren generierten Bildern einen Media-Eintrag bei Twitter zu erstellen (v1.1) und einen Tweet mit dem Media und einer Beschreibung zu erstellen und zu veröffentlichen. 

Hierfür mussten wir einen Twitter Developer-Account erstellen um Zugang zum Developer Portal zu erhalten. Dort wurde ein neues Projekt mit einer neuen App (socialtunes_2023) angelegt. Wir haben für die App die Authentifizierungs-Einstellungen angepasst um sowohl OAuth 1.0a als auch OAuth 2.0 zu aktivieren. 

Für 1.0a wurden die Zugriffsberechtigungen auf "Read and write" festgelegt, für 2.0 wurde die Art der App als Web App mit einem confidential client festgelegt. Zudem wurde die URL der Webseite und eine Callback URL angegeben. Danach wurden die benötigten Keys und Tokens generiert und in die Anwendung integriert. 

Für die Anbindung an Twitter haben wir das Python Package tweepy genutzt.

### Deezer
Mit dieser gab es ein paar Schwierigkeiten. Es war schwer die ISRC von dem entsprechenden Song
abzurufen. Auch ist zu erwähnen, dass es nicht möglich war, die ganze List von den Songs auf einmal zu Convertieren, sondern man musste immer auf das erste Element
zugreifen.

## Zugansdaten der Entwicklungsaccounts
| Dienst | Nutzername/Mail | Passwort |
| ------ | ------ | ------ |
|Google Account|socialtunes.test@gmail.com|Socialtunes123456.|

Anmelde Daten für weitere APIs sind über Google Anmeldungen Funktional. Bei Twitter muss man sich zunächst bei Twitter selbst auf der Seite anmelden, da in dem Google Account das Passwort nicht richtig gespeichert wurde.
