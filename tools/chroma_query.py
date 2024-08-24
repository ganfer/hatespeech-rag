import chromadb

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")

# Ask user for Input
user_input = input("Bitte geben Sie einen Satz zum Suchen ein: ")

# Query in ChromaDB 
results = collection.query(
    query_texts=[user_input],
    n_results=1
)

print(results)