import chromadb

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")

# Add documents to collection
collection.upsert(
    documents=[
        "[Target] sind eine Plage und gehören weg!", 
        "Alle Anhänger von [Target] sind gefährlich!",
        "[Target] können das nicht richtig machen.", 
    ],
    metadatas=[
        {"Label": " Hatespeech", "Target": "Fremdenfeindlichkeit"},
        {"Label": " Hatespeech", "Target": "Antisemitismus"},
        {"Label": " Hatespeech", "Target": "Sexismus"},
    ],
    ids=["id1", "id2", "id3"]
)

# Query collection (for testing purposes)
results = collection.query(
    query_texts=["Alle Anhänger des [Target] sind ätzend!"],
    n_results=1
)
print(results)