# RAG Marseille

Guide touristique intelligent de Marseille propulsé par l'IA.
Pose une question sur Marseille, obtiens une réponse personnalisée basée sur **148 lieux réels** issus de Google Places.

## Fonctionnement
Question utilisateur
↓
API Flask
↓
ChromaDB recherche les lieux pertinents (recherche sémantique)
↓
GPT-3.5 génère une réponse basée sur ces lieux
↓
Réponse + sources affichées

## Stack technique

| Technologie | Rôle |
|---|---|
| Python / Flask | API REST |
| ChromaDB | Base de données vectorielle |
| OpenAI GPT-3.5 | Génération de réponses |
| Google Places API | Source des données (148 lieux) |
| Docker / Docker Compose | Conteneurisation |

## Lancer le projet en local

### Prérequis
- Docker Desktop installé
- Une clé API OpenAI — platform.openai.com
- Une clé API Google Places — console.cloud.google.com

### Installation

1. Clone le projet

```bash
git clone https://github.com/louis-varennes/rag-marseille.git
cd rag-marseille
```

2. Crée le fichier `.env`
OPENAI_API_KEY=ta_cle_openai
GOOGLE_PLACES_API_KEY=ta_cle_google

3. Lance avec Docker

```bash
docker compose up
```

4. Ouvre dans le navigateur
http://localhost:5002

Au démarrage, l'API charge automatiquement **148 lieux** depuis Google Places et les indexe dans ChromaDB.

## API — Routes disponibles

### Interface web
GET /

### Poser une question
```bash
curl -X POST http://localhost:5002/question \
  -H "Content-Type: application/json" \
  -d '{"question": "Où manger une bouillabaisse à Marseille ?"}'
```

### Ajouter un lieu manuellement
```bash
curl -X POST http://localhost:5002/ajouter \
  -H "Content-Type: application/json" \
  -d '{"lieu": "Description du lieu..."}'
```

### Statut de l'API
```bash
curl http://localhost:5002/status
```

## Structure du projet
rag-marseille/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app.py
├── .env               <- clés API (non versionné)
├── .gitignore
└── templates/
└── index.html

## Auteur

**Louis Varennes** — étudiant Développeur IA & Data
LaPlateforme Marseille — promotion 2025
github.com/louis-varennes