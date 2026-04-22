import os
import time
import requests
import chromadb
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
GOOGLE_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

def get_collection():
    retries = 5
    while retries > 0:
        try:
            client = chromadb.HttpClient(host="chromadb", port=8000)
            collection = client.get_or_create_collection("marseille")
            return collection
        except Exception as e:
            print(f"ChromaDB pas encore prêt, retry dans 2s... ({e})")
            retries -= 1
            time.sleep(2)
    raise Exception("Impossible de se connecter à ChromaDB")

def charger_lieux_google():
    collection = get_collection()
    if collection.count() > 0:
        print(f"{collection.count()} lieux déjà dans ChromaDB, chargement ignoré")
        return

    print("Chargement des lieux depuis Google Places...")
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    requetes = [
        "bars et pubs Marseille",
        "restaurants Marseille",
        "musées Marseille",
        "plages Marseille",
        "monuments historiques Marseille",
        "lieux culturels Marseille",
        "parcs et jardins Marseille",
        "quartiers à visiter Marseille",
    ]

    documents = []
    ids_set = set()
    compteur = 0

    for requete in requetes:
        params = {
            "query": requete,
            "language": "fr",
            "key": GOOGLE_API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        for place in data.get("results", []):
            place_id = place.get("place_id", "")
            if place_id in ids_set:
                continue

            ids_set.add(place_id)
            nom = place.get("name", "")
            adresse = place.get("formatted_address", "")
            types = ", ".join(place.get("types", []))
            note = place.get("rating", "non noté")
            description = f"{nom} est situé à {adresse}. Type : {types}. Note Google : {note}/5."
            documents.append(description)
            compteur += 1

        print(f"'{requete}' → {len(data.get('results', []))} résultats")
        time.sleep(0.5)

    if documents:
        ids = [f"google_{i}" for i in range(len(documents))]
        collection.add(documents=documents, ids=ids)
        print(f"{compteur} lieux uniques ajoutés dans ChromaDB")

@app.route("/")
def accueil():
    return render_template("index.html")

@app.route("/status")
def status():
    collection = get_collection()
    return jsonify({
        "message": "RAG Marseille en ligne !",
        "lieux_en_base": collection.count()
    })

@app.route("/question", methods=["POST"])
def question():
    data = request.get_json()
    question_utilisateur = data.get("question")
    collection = get_collection()
    resultats = collection.query(
        query_texts=[question_utilisateur],
        n_results=3
    )
    documents_pertinents = resultats["documents"][0]
    contexte = "\n".join(documents_pertinents)
    reponse = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un guide local expert de Marseille. Réponds de façon précise et enthousiaste en te basant uniquement sur le contexte fourni. Si la réponse n'est pas dans le contexte, dis-le honnêtement."},
            {"role": "user", "content": f"Contexte:\n{contexte}\n\nQuestion: {question_utilisateur}"}
        ]
    )
    return jsonify({
        "question": question_utilisateur,
        "reponse": reponse.choices[0].message.content,
        "sources": documents_pertinents
    })

@app.route("/ajouter", methods=["POST"])
def ajouter():
    data = request.get_json()
    lieu = data.get("lieu")
    if not lieu:
        return jsonify({"erreur": "Le champ 'lieu' est requis"}), 400
    collection = get_collection()
    nouvel_id = f"manuel_{collection.count()}"
    collection.add(documents=[lieu], ids=[nouvel_id])
    return jsonify({
        "message": "Lieu ajouté avec succès",
        "id": nouvel_id,
        "lieu": lieu,
        "total_lieux": collection.count()
    })

if __name__ == "__main__":
    charger_lieux_google()
    app.run(host="0.0.0.0", port=5000)