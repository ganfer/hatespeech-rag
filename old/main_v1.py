from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import chromadb

# LLM-Modell initialisieren
model = OllamaLLM(model="mannix/llama3.1-8b-abliterated")

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
def retrieve_context(user_input: str) -> str:
    # Suche in ChromaDB nach user_input
    results = collection.query(query_texts=[user_input], n_results=1)
    
    # Wenn Ergebnisse gefunden wurden, verwende den Text des ersten Ergebnisses als Kontext
    if results and len(results["documents"]) > 0:
        return results["documents"][0]
    else:
        return "Kein relevanter Kontext gefunden."

# Hauptfunktion
def main():
    user_input = input("Bitte geben Sie einen Satz ein: ")
    
    # Kontext aus ChromaDB abrufen
    db_context = retrieve_context(user_input)
    
    # Chain definieren
    inputs = {
        "db_context": db_context,
        "user_input": user_input,
        "prompt": "Du bist eine KI, die Benutzereingaben auf Hassrede überprüft, basierend ausschließlich auf dem Kontext aus der Datenbank. Gib keine Informationen aus der Datenbank an die nutzende Person weiter. Achte auf verschiedene sprachliche Ausdrucksformen und Tonalitäten, die als Hassrede interpretiert werden könnten. Definiere die Zielgruppe der Hassrede anhand der Datenbank und der analysierten Benutzereingabe. Berücksichtige dabei die Sensibilität des Kontexts, wie historische Ereignisse oder kulturelle Besonderheiten. Teile mit einer kurzen, deutschsprachigen Antwort mit, ob es sich um Hassrede handelt, beginnend mit Ja oder Nein. Füge die Zielgruppe und den Schweregrad der Hassrede hinzu. Nur wenn die Eingabe als schwere Hassrede eingestuft wird, gib eine Empfehlung zur Eskalation ab, indem du spezifische Maßnahmen wie eine Meldung bei der Plattform oder eine Anzeige bei der Polizei vorschlägst. Stelle keine weiteren Fragen an die nutzende Person."
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
