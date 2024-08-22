import chromadb

chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")

# Alle Dokumente in der Sammlung abrufen
documents = collection.get()

print("Gespeicherte Dokumente und ihre IDs:")
for doc, id_ in zip(documents['documents'], documents['ids']):
    print(f"ID: {id_}, Dokument: {doc}")

# Anzahl der Dokumente ermitteln
num_documents = len(documents['documents'])

print(f"Gesamtanzahl der gespeicherten Dokumente: {num_documents}")