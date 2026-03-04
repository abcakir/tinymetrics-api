# TinyMetrics

Ein schlanker URL-Shortener mit FastAPI und PostgreSQL, optimiert für AWS-Umgebungen.

## Features
* Shortlinks über `/s/` Präfix (z.B. `domain.com/s/xyz`)
* GitHub OAuth & JWT Authentifizierung
* Klick-Analytics im Backend
* Vollständig containerisiert mit Docker

## Tech Stack
FastAPI, PostgreSQL, Docker, Angular, Tailwind CSS

## Deployment auf AWS
Das Projekt läuft auf einer EC2 Instanz hinter einem **Nginx Proxy Manager**. 

* **SSL:** Automatische Zertifikate via Let's Encrypt.
* **Ports:** In der AWS Security Group müssen nur 80, 443 und 22 offen sein.
* **Routing:** Anfragen an `/api` und `/s/` gehen an das Backend, der Rest an das Frontend.

## Start
```bash
git clone https://github.com/abcakir/tinymetrics-api.git
docker compose up -d --build
```

## Tests

```bash
docker compose exec app pytest
```
