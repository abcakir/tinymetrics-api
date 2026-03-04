# TinyMetrics API

Ein leistungsstarker URL-Shortener mit Fokus auf Cloud-Deployment, Analytics und sicherer Authentifizierung.

---

## Kernfunktionen

- **URL Shortening**: Generierung eindeutiger Kurz-Links über dedizierte `/s/` Pfade.
- **Analytics**: Echtzeit-Tracking von Klicks und Metadaten.
- **Authentifizierung**: Sichere Anmeldung via JWT und GitHub OAuth2.
- **Infrastruktur**: Optimiert für Docker-Umgebungen hinter Reverse-Proxies.

---

## Tech Stack

| Bereich | Technologie |
|--------|-------------|
| **Backend** | FastAPI (Python 3.11+), SQLAlchemy |
| **Datenbank** | PostgreSQL |
| **DevOps** | Docker, Docker Compose, Nginx Proxy Manager |
| **Testing** | Pytest |

---

## Setup & Deployment

### Voraussetzungen

- Docker und Docker Compose installiert
- GitHub OAuth Application (für Social Login)

### Installation

**1. Repository klonen**

```bash
git clone https://github.com/abcakir/tinymetrics-api.git
cd tinymetrics-api
```

**2. Umgebungsvariablen konfigurieren**

Erstelle eine `.env` Datei im Hauptverzeichnis:

```env
DATABASE_URL=postgresql://tinyuser:password@db:5432/tinymetrics
SECRET_KEY=dein_geheimer_schluessel
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GITHUB_CLIENT_ID=deine_id
GITHUB_CLIENT_SECRET=dein_secret
```

**3. Container starten**

```bash
docker compose up -d --build
```

---

## Deployment & Sicherheit

### AWS EC2 Hosting

Das Projekt ist für den Betrieb auf einer AWS EC2 Instanz (z. B. `t2.micro`) konfiguriert.

- **Security Groups**: Für den Live-Betrieb müssen die Ports `80` (HTTP), `443` (HTTPS) und `22` (SSH) freigegeben sein.
- **Orchestrierung**: Dank Docker Compose lassen sich Frontend, Backend und Datenbank konsistent bereitstellen.

### SSL & Zertifikate (Let's Encrypt)

Die Absicherung erfolgt über den **Nginx Proxy Manager (NPM)**:

- **Automatische Zertifikate**: SSL-Zertifikate werden via Let's Encrypt generiert und automatisch erneuert.
- **HTTPS Enforcement**: Der Proxy erzwingt verschlüsselte Verbindungen für die API, das Dashboard und die Redirects.
- **Routing**: Anfragen an `/api` und `/s/` werden gezielt an den Backend-Container geleitet, während alle anderen Pfade das Frontend bedienen.

---

## Testing

Die Testsuite wird innerhalb der Docker-Umgebung ausgeführt:

```bash
docker compose exec app pytest
```
