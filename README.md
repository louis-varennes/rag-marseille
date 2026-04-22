# 🗺️ RAG Marseille

Guide touristique intelligent de Marseille propulsé par l'IA.
Pose une question sur Marseille, obtiens une réponse personnalisée basée sur de vraies données.

## 🛠️ Technologies

- **Python / Flask** — API REST
- **ChromaDB** — base de données vectorielle
- **OpenAI GPT-3.5** — génération de réponses
- **Google Places API** — données des lieux
- **Docker / Docker Compose** — conteneurisation

## 🚀 Lancer le projet

### Prérequis
- Docker Desktop installé
- Une clé API OpenAI
- Une clé API Google Places

### Installation

1. Clone le projet
\```bash
git clone https://github.com/ton-username/rag-marseille.git
cd rag-marseille
\```

2. Crée le fichier `.env`
\```bash
OPENAI_API_KEY=ta_cle_openai
GOOGLE_PLACES_API_KEY=ta_cle_google
\```

3. Lance avec Docker
\```bash
docker compose up
\```

L'API est disponible sur `http://localhost:5002`

## 📡 Utilisation

### Poser une question
\```bash
curl -X POST http://localhost:5002/question \
  -H "Content-Type: application/json" \
  -d '{"question": "Où manger une bouillabaisse à Marseille ?"}'
\```

### Ajouter un lieu
\```bash
curl -X POST http://localhost:5002/ajouter \
  -H "Content-Type: application/json" \
  -d '{"lieu": "Description du lieu..."}'
\```

### Vérifier l'état de l'API
\```bash
curl http://localhost:5002/
\```

## 🏗️ Architecture