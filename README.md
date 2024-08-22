# hatespeech-rag
This RAG is designed to analyze user inputs for potential hate speech using a combination of a language model (LLM) and a ChromaDB database. The LLM evaluates the input against a curated database of hate speech entries, determining whether the input should be classified as such. If the input is identified as hate speech and sufficiently distinct from existing entries in the database, it is stored for future reference. The script also ensures that redundant entries are avoided, maintaining the efficiency and relevance of the database.

## Install the Requirements
clone git and install ollama locally.

Python:
pip install -r requirements/requirements.txt

Ollama:
ollama pull mannix/llama3.1-8b-abliterated
> :warning: **Uncensored**: Please use uncensored versions of Llama, such as Mannix Llama 3.1; otherwise, this script will not function properly.

## Initial Load to ChromaDB

Use one of the following scripts:
- The `initial_load_csv.py` script imports the CSV file stored in `/data` to update the Chroma database.
- The `initial_load_ai.py` script prompts Ollama to generate hate speech examples and updates the Chroma database.

## Run main.py

This Python script combines the use of a language model (LLM) with a ChromaDB database to review user inputs for group-based hostility (hate speech) and, if applicable, store them. This helps to expand the database with new, pertinent examples of hate speech while avoiding redundant or identical entries.


#### Script Workflow:

 **Initialization:**
   - An LLM model (`OllamaLLM`) and a ChromaDB database (`hatespeech`) are initialized. The model is used to analyze user inputs, while the database is used to find similar entries and store new ones.

 **Prompt Creation:**
   - A specific prompt is defined for the LLM, instructing the model on how to evaluate the user input for hate speech. The prompt details how the analysis should be conducted and what information the LLM should consider in its response.

 **Query and Context Matching:**
   - A function, `retrieve_context_and_distances`, searches the ChromaDB for similar entries based on the user input. The function returns documents and the distances of these documents to the input.

 **LLM Invocation:**
   - The user input and relevant context from the database are sent to the LLM. The LLM then responds, determining whether the input should be classified as hate speech.

 **Database Storage:**
   - If the LLM identifies the input as hate speech and the distance to similar entries in the database exceeds a certain threshold, the input is stored in the database.

 **User Feedback:**
   - The LLM's response is printed, and depending on the classification, the input is either stored in the database or ignored.

## Tools

Don`t forgt to use the other tools.

- `chroma_query.py`
This script is designed to query the database and retrieve specific information based on user input.
- `chroma_inspector.py`
This script provides an overview of your ChromaDB database, displaying the contents and the total number of documents stored.

## old

- `main_v1.py` is the first edition of the script. The new main.py is fully updated to include database writeback functionality and integration with Llama 3.1.
- `chroma_query_v1.py` is the initial version of the query script. The latest version in `/tools` includes console input functionality.
