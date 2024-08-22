import chromadb
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")
results = collection.query(
    query_texts=["Die haben kein Recht zu leben."],
    n_results=1
)
print(results)