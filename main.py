from rag_assistant import RagAssistant
from event_handler import EventHandler
from vector_store_handler import VectorStoreHandler

api_key = ""  # Sostituisci con il tuo API key
#vector_store_id = "vs_CDyUZzbIzgnvV3a2HNTfMM2w"  # Sostituisci con il tuo vector store ID, se disponibile

docs = ["Rag_demo\\Documenti\\Contratto.pdf", "Rag_demo\\Documenti\\AccordoLavoroAgile.pdf"]

rag_assistant = RagAssistant(api_key=api_key, vector_store_id=None)
VectorStoreHandler.add_documents(rag_assistant.client , rag_assistant.vector_store_id, documents= docs)
rag_assistant.create_thread()

# Continuare la conversazione nel terminale
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = rag_assistant.continue_thread(user_input)
    print(f"Assistant: {response}")