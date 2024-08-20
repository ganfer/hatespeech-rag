from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import chromadb

# LLM-Modell initialisieren
model = OllamaLLM(model="llama2-uncensored")

# ChromaDB-Client initialisieren
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")

# Template für die Eingabeaufforderung definieren
template = """Beantworte die Frage basierend auf folgendem Kontext:
Kontext aus der Datenbank: {db_context}

Benutzereingabe: {user_input}

Prompt: {prompt}
"""

prompt = ChatPromptTemplate.from_template(template)

# Funktion zum Abrufen des Kontextes aus ChromaDB
def retrieve_context(argument: str) -> str:
    # Suche in der ChromaDB nach dem Argument
    results = collection.query(query_texts=[argument], n_results=1)
    
    # Wenn Ergebnisse gefunden wurden, verwende den Text des ersten Ergebnisses als Kontext
    if results and len(results["documents"]) > 0:
        return results["documents"][0]
    else:
        return "Kein relevanter Kontext gefunden."

# Hauptfunktion
def main():
    argument = input("Bitte geben Sie einen Satz ein: ")
    
    # Kontext aus ChromaDB abrufen
    db_context = retrieve_context(argument)
    
    # Chain definieren
    inputs = {
        "db_context": db_context,
        "user_input": argument,
        "prompt": "Prüfe, ob es bei der Benutzereingabe um Hassrede handelt. Vergleiche es mit dem Kontext aus der Datenbank. Gebe weitere Informationen wie die Zielgruppe und den Schweregrad mit. Antworte nur auf deutsch."
    }
    
    # Prompt mit Kontext und Frage füllen
    prompt_value = prompt.invoke(inputs)
    
    # Den Prompt in einen String konvertieren
    prompt_text = str(prompt_value)
    
    # LLM anfragen mittels `invoke`
    response = model.invoke(prompt_text)
    
    # Antwort ausgeben
    print(response)

if __name__ == "__main__":
    main()
