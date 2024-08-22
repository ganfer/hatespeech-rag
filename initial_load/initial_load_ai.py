import chromadb
import uuid
from langchain_ollama.llms import OllamaLLM

# Initialisiere das LLM Modell
model = OllamaLLM(model="mannix/llama3.1-8b-abliterated")
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech_kategorien")

# Funktion, um Hassrede-Kategorien von llama3 zu generieren
def generate_hate_speech_categories(model, prompt="Gebe alle Sätze auf deutsch aus, die als gruppenbezogene Menschenfeindlichkeit (Hassrede) identifiziert werden können. Wichtig ist, dass in jeder Aussage eine Zielgruppe existiert. Nutze keine Überschriften oder Aufzählungszeichen wie Zahlen oder Strichpunkte, beginne aber nach jeder Aussage eine neue Zeile."):
    response = model.invoke(prompt)  # Nutzung von invoke statt __call__
    return response.splitlines()

# Generiere Kategorien von Hassreden
categories_list = generate_hate_speech_categories(model)

# Füge die Kategorien in die Datenbank ein
for category in categories_list:
    if category:  # Nur nicht-leere Kategorien hinzufügen
        unique_id = str(uuid.uuid4())  # Generiere eine eindeutige ID
        collection.add(documents=[category], ids=[unique_id])

# Alle Dokumente in der Sammlung abrufen
documents = collection.get()

print("Gespeicherte Dokumente und ihre IDs:")
for doc, id_ in zip(documents['documents'], documents['ids']):
    print(f"ID: {id_}, Dokument: {doc}")
