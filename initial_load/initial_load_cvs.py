import pandas as pd
import chromadb

# ChromaDB-Client initialisieren
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")

# Excel Datei einlesen
file_path = './data/hatespeech.xlsx'
df = pd.read_excel(file_path)

#Daten extrahieren und konvertieren
documents = df['argument'].tolist()
metadatas = df[['label', 'target']].to_dict(orient='records')
ids = df['id'].astype(str).tolist()

# Hinzufügen zur Chroma DB
collection.upsert(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
)
