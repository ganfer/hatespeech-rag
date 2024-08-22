# hatespeech-rag
This RAG is designed to analyze user inputs for potential hate speech using a combination of a language model (LLM) and a ChromaDB database. The LLM evaluates the input against a curated database of hate speech entries, determining whether the input should be classified as such. If the input is identified as hate speech and sufficiently distinct from existing entries in the database, it is stored for future reference. The script also ensures that redundant entries are avoided, maintaining the efficiency and relevance of the database.

## Install the Requirements

Python
pip install -r requirements/requirements.txt

Ollama
ollama pull mannix/llama3.1-8b-abliterated

## Create a initial load.
Use the CSV or AI Script to update database

## run main.py

This Python script combines the use of a language model (LLM) with a ChromaDB database to review user inputs for group-based hostility (hate speech) and, if applicable, store them.

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

#### Purpose:
The script is designed to assess user inputs for hate speech and, if recognized as relevant and new, store them in a database. This helps to expand the database with new, pertinent examples of hate speech while avoiding redundant or identical entries.

## Tools
Don`t forgt to use the other tools.
**chroma query**
This script is designed to query the database and retrieve specific information based on user input.
**chroma inspector**
This script provides an overview of your ChromaDB database, displaying the contents and the total number of documents stored.

## old
`main_v1.py` is the first edition of the script, the new main is fully updated to include database writeback functionality and integration with Llama 3.1.