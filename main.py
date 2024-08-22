from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import chromadb
import uuid

# LLM-Modell und ChromaDB-Client initialisieren
model = OllamaLLM(model="mannix/llama3.1-8b-abliterated")
# Chroma initialisieren
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")

# Template für das LLM definieren
prompt_template = """Beantworte die Frage basierend auf folgendem Kontext:
Kontext aus der Datenbank: {db_context}

Benutzereingabe: {user_input}

Prompt: {prompt}
"""
prompt = ChatPromptTemplate.from_template(prompt_template)

# Funktion zum Abrufen von Kontext und Distanzen aus ChromaDB
def retrieve_context_and_distances(user_input: str):
    results = collection.query(query_texts=[user_input], n_results=5)
    return results["documents"], results["distances"] if results["documents"] else (None, None)

# Funktion zum Speichern des Benutzerinputs in ChromaDB
def store_user_input(user_input: str):
    collection.upsert(documents=[user_input], ids=[str(uuid.uuid4())])
#    print(f"Ihre Eingabe '{user_input}' wurde in unserer Datenbank gespeichert. Vielen Dank für Ihre Mitwirkung.")

# Hauptfunktion
def main():
    user_input = input("Bitte geben Sie einen Satz ein: ")
    db_contexts, distances = retrieve_context_and_distances(user_input)

    # LLM aufrufen
    response = model.invoke(str(prompt.invoke({
        "db_context": db_contexts[0] if db_contexts else "Kein relevanter Kontext gefunden.",
        "user_input": user_input,
        "prompt": "Du bist eine KI, die Benutzereingaben auf gruppenbezogene Menschenfeindlichkeit (Hassrede) überprüft. Aufgabe: Überprüfe die Benutzereingabe basierend auf dem Kontext der Datenbank, die Hassrede enthält. Wenn ein Datensatz mit ausreichender Ähnlichkeit in der Datenbank vorhanden ist, gilt die Eingabe automatisch als Hassrede. Diskretion: Gib keine Informationen aus der Datenbank direkt an die nutzende Person weiter. Erkennung von Hassrede: Analysiere die Benutzereingabe sorgfältig und achte auf verschiedene sprachliche Ausdrucksformen und Tonalität, die als Hassrede interpretiert werden könnten. Zielgruppendefinition: Bestimme anhand der Datenbank und der Benutzereingabe, welche Zielgruppe von der Hassrede betroffen ist. Kontextuelle Sensibilität: Berücksichtige historische Ereignisse, kulturelle Besonderheiten und den Kontext der Datenbank bei deiner Analyse. Antwort: Gib eine kurze, deutschsprachige Antwort, die mit Ja oder Nein beginnt, ob es sich um Hassrede handelt. Falls Ja, füge die Zielgruppe und den Schweregrad der Hassrede hinzu. Nur wenn es sich um schwere Hassrede handelt, empfehle konkrete Eskalationsmaßnahmen, wie eine Meldung bei der Plattform oder eine Anzeige bei der Polizei. Wichtig: Stelle keine weiteren Fragen an die nutzende Person."
    })))

    # Die Antwort des LLM ausgeben
    print(f"Antwort des LLM: {response}")

    if "Ja" in response:
        # Nur speichern, wenn die Distanz klein genug ist (ähnlich, aber nicht identisch)
        if not db_contexts or any(min(dist) > 0.01 for dist in distances):
            store_user_input(user_input)
    #    else:
    #        print("Der Satz ist in ähnlicher Form in unserer Datenbank vorhanden.")
    #else:
    #    print("Der Satz wurde nicht als Hassrede erkannt und wird daher nicht gespeichert.")

if __name__ == "__main__":
    main()