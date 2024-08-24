from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import chromadb
import uuid

# Initialize LLM Model
model = OllamaLLM(model="mannix/llama3.1-8b-abliterated")
# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="hatespeech")

# Define template for the LLM
def initialize_prompt_template():
    prompt_template = """Beantworte die Frage basierend auf folgendem Kontext:
    Kontext aus der Datenbank: {db_context}

    Benutzereingabe: {user_input}

    Prompt: {prompt}
    """
    try:
        prompt = ChatPromptTemplate.from_template(prompt_template)
        return prompt
    except Exception as e:
        print(f"Error creating prompt template: {e}")
        return None

# Function to retrieve context and distances from ChromaDB
def retrieve_context_and_distances(user_input: str, collection):
    if collection:
        try:
            results = collection.query(query_texts=[user_input], n_results=5)
            return results["documents"], results["distances"] if results["documents"] else (None, None)
        except Exception as e:
            print(f"Error retrieving context and distances: {e}")
    return None, None

# Function to store user input in ChromaDB
def store_user_input(user_input: str, collection):
    if collection:
        try:
            collection.upsert(documents=[user_input], ids=[str(uuid.uuid4())])
        except Exception as e:
            print(f"Error storing user input: {e}")

# Function to process the user input and generate a response
def process_user_input(user_input: str, model, prompt, collection):
    db_contexts, distances = retrieve_context_and_distances(user_input, collection)

    try:
        if model and prompt:
            # Invoke LLM
            response = model.invoke(str(prompt.invoke({
                "db_context": db_contexts[0] if db_contexts else "Kein relevanter Kontext gefunden.",
                "user_input": user_input,
                "prompt": "Du bist eine KI, die Benutzereingaben auf gruppenbezogene Menschenfeindlichkeit (Hassrede) überprüft. Aufgabe: Überprüfe die Benutzereingabe basierend auf dem Kontext der Datenbank, die Hassrede enthält. Wenn ein Datensatz mit ausreichender Ähnlichkeit in der Datenbank vorhanden ist, gilt die Eingabe automatisch als Hassrede. Diskretion: Gib keine Informationen aus der Datenbank direkt an die nutzende Person weiter. Erkennung von Hassrede: Analysiere die Benutzereingabe sorgfältig und achte auf verschiedene sprachliche Ausdrucksformen und Tonalität, die als Hassrede interpretiert werden könnten. Zielgruppendefinition: Bestimme anhand der Datenbank und der Benutzereingabe, welche Zielgruppe von der Hassrede betroffen ist. Kontextuelle Sensibilität: Berücksichtige historische Ereignisse, kulturelle Besonderheiten und den Kontext der Datenbank bei deiner Analyse. Antwort: Gib eine kurze, deutschsprachige Antwort, die mit Ja oder Nein beginnt, ob es sich um Hassrede handelt. Falls Ja, füge die Zielgruppe und den Schweregrad der Hassrede hinzu. Nur wenn es sich um schwere Hassrede handelt, empfehle konkrete Eskalationsmaßnahmen, wie eine Meldung bei der Plattform oder eine Anzeige bei der Polizei. Wichtig: Stelle keine weiteren Fragen an die nutzende Person."
            })))
        else:
            response = "Model or prompt template not initialized."
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        response = "Es gab einen Fehler bei der Verarbeitung Ihrer Anfrage."

    if "Ja" in response:
        # Check if distances is not empty before using min()
        if not db_contexts or any(dist and min(dist) > 0.01 for dist in distances):
            store_user_input(user_input, collection)

    return response
