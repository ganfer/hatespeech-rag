import chromadb
# ChromaDB-Client initialisieren
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")
# Suche starten
results = collection.query(
    query_texts=["[Suchwort]]"],
    n_results=1
)
print(results)