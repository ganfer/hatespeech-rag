import chromadb
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")
results = collection.query(
    query_texts=["Ich hasse Juden."],
    n_results=1
)

print(results)