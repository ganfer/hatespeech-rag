import chromadb

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")

# Get all documents from collection
documents = collection.get()

print("Gespeicherte Dokumente und ihre IDs:")
for doc, id_ in zip(documents['documents'], documents['ids']):
    print(f"ID: {id_}, Dokument: {doc}")

# Get number of documents
num_documents = len(documents['documents'])

print(f"Gesamtanzahl der gespeicherten Dokumente: {num_documents}")