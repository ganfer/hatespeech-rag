import chromadb
chroma_client = chromadb.PersistentClient(path="./chromadb")

collection = chroma_client.get_or_create_collection(name="hatespeech")


collection.upsert(
    documents=[
        "[Target] sind eine Plage und gehören weg!", 
        "Alle Anhänger von [Target] sind gefährlich!",
        "[Target] können das nicht richtig machen.", 
    ],
    metadatas=[
        {"Label": " Hatespeech", "Target": "Ethnie"},
        {"Label": " Hatespeech", "Target": "Religion"},
        {"Label": " Hatespeech", "Target": "Geschlecht"},
    ],
    ids=["id1", "id2", "id3"]
)

results = collection.query(
    query_texts=["Alle Anhänger des Islams sind ätzend!"],
    n_results=1
)

print(results)
