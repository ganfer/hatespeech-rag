import chromadb
import uuid
from langchain_ollama.llms import OllamaLLM

# Initialisiere ChromaDB
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")

# Initialisiere das LLM Modell
model = OllamaLLM(model="mannix/llama3.1-8b-abliterated")

# Funktion, um Hassrede von llama generieren zu lassen
def generate_hate_speech(model, prompt="Gebe weitere 10 Sätze auf deutsch aus, die als gruppenbezogene Menschenfeindlichkeit (Hassrede) identifiziert werden können. Wichtig ist, dass in jeder Aussage eine Zielgruppe existiert. Nutze keine Überschriften oder Aufzählungszeichen wie Zahlen oder Strichpunkte, beginne aber nach jeder Aussage eine neue Zeile."):
    response = model.invoke(prompt)
    return response.splitlines()

# Generiere Hassrede
hatespeech_list = generate_hate_speech(model)

# Füge die Hassrede in die Datenbank ein
for hatespeech in hatespeech_list:
    if hatespeech:  # Nur nicht-leere Sätze hinzufügen
        unique_id = str(uuid.uuid4())  # Generiere eine eindeutige ID
        collection.upsert(documents=[hatespeech], ids=[unique_id])
#        print(hatespeech)

# Alle Dokumente in der Sammlung abrufen
#documents = collection.get()

#print("Gespeicherte Dokumente und ihre IDs:")
#for doc, id_ in zip(documents['documents'], documents['ids']):
#    print(f"ID: {id_}, Dokument: {doc}")
