# RoadSense

Projet de détection et d'analyse de l'état des routes.

## Architecture

Le projet est composé de plusieurs microservices :
- **Dashboard** : Frontend (React/Vite)
- **RoadSense Core** : API principale (FastAPI)
- **Ingestion Video** : Traitement des vidéos (FastAPI)
- **Detection Fissures** : Analyse d'images par IA (FastAPI/PyTorch)
- **Georef** : Géoréférencement (FastAPI)
- **Score Gravité** : Calcul de score (FastAPI)
- **Prioritisation** : Logique de priorité (FastAPI)
- **Export SIG** : Export de données (FastAPI)

## Prérequis

### Option 1 (Recommandée) : Docker
La méthode la plus simple pour lancer le projet est d'utiliser Docker.
- **Docker Desktop** installé et lancé.

### Option 2 : Installation Manuelle
Si vous souhaitez lancer les services individuellement sans Docker :
- **Python 3.10+**
- **Node.js 18+** & **npm**
- **PostgreSQL 16** (avec extension PostGIS)
- **MinIO** (ou accès S3)

## Lancement (Docker)

À la racine du projet, exécutez :

```bash
docker-compose up --build
```

Cette commande va construire les images et lancer tous les services, y compris la base de données et le stockage objet.

## Accès

- **Dashboard** : http://localhost:5173 (ou le port configuré dans docker-compose, souvent 80 ou 3000, vérifiez les logs)
    - *Note : Dans le docker-compose actuel, le dashboard n'est pas explicitement exposé ou est en cours de développement. Vérifiez le dossier `dashboard` pour le lancer manuellement si besoin (`npm run dev`).*
- **Portainer / Admin DB** : (Si configuré)
- **MinIO Console** : http://localhost:9001 (User: minio, Pass: minio123)

## Développement Local

Pour le Dashboard :
```bash
cd dashboard
npm install
npm run dev
```

Pour un service Python (ex: roadsense-core) :
```bash
cd roadsense-core
pip install -r requirements.txt
uvicorn main:app --reload
```
