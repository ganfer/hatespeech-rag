from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import chromadb

# Initialisiere das Modell
model = OllamaLLM(model="llama3.1")

# Funktion zur Einbettung und Suche in ChromaDB
def search_in_chromadb(argument, similarity_threshold=0.8):
    # Text einbetten (Embedding)
    embedded_vector = model.embed(text=argument)

    # ChromaDB Abfrage
    chroma_client = chromadb.PersistentClient(path="./chromadb")
    collection = chroma_client.get_or_create_collection(name="hatespeech")

    # Suche nach ähnlichen Vektoren in der Collection
    results = collection.query(
        query_embeddings=[embedded_vector],
        n_results=5  # Anzahl der zurückgegebenen Ergebnisse
    )

    # Filtern der Ergebnisse basierend auf dem Ähnlichkeitsscore (z.B. Cosinus-Ähnlichkeit)
    filtered_results = [
        (doc, score) for doc, score in zip(results['documents'], results['distances'])
        if score <= similarity_threshold
    ]

    return filtered_results

# Funktion zur Überprüfung auf Hate Speech
def check_for_hatespeech(argument):
    # Suche in ChromaDB mit einem Ähnlichkeitsschwellenwert
    similar_documents = search_in_chromadb(argument)

    # Überprüfen, ob ähnliche Dokumente gefunden wurden
    if not similar_documents:
        return "Keine ausreichend ähnlichen Dokumente gefunden."

    # Führe die Kette mit den gefundenen Dokumenten aus
    template = """Argument: {argument}

    Gefundene ähnliche Dokumente:
    {documents}

    Frage: Handelt es sich um Hate Speech?"""
    
    # Liste der gefundenen ähnlichen Dokumente
    documents_text = "\n".join([doc for doc, _ in similar_documents])
    
    # Prompt mit den gefundenen Dokumenten vorbereiten
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    # LLM-Abfrage
    response = chain.invoke({
        "argument": argument,
        "documents": documents_text
    })

    return response

# Beispiel-Argument
argument = "Alle Anhänger des Islams sind ätzend!"

# Überprüfung auf Hate Speech
result = check_for_hatespeech(argument)

# Ergebnis ausgeben
print(result)
