import pandas as pd
import chromadb

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")

# Read Excel file
file_path = './data/hatespeech.xlsx'
df = pd.read_excel(file_path)

# Extract and convert data
documents = df['argument'].tolist()
metadatas = df[['label', 'target']].to_dict(orient='records')
ids = df['id'].astype(str).tolist()

# Add to ChromaDB
collection.upsert(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
)