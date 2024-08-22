import chromadb
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")
results = collection.query(
    query_texts=["[HASSREDE HIER EINFÜGEN]"],
    n_results=1
)

print(results)