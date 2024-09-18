from openai import OpenAI

class RagAssistant:
    def __init__(self, api_key, vector_store_id=None):
        self.client = OpenAI(api_key=api_key)

        # Creare un Assistant con File Search abilitato
        self.assistant = self.client.beta.assistants.create(
            name="RAG Assistant",
            instructions="Sei un assistente utile ed intelligente che estrae informazioni da documenti dati",
            model="gpt-4o",
            tools=[{"type": "file_search"}],
        )

        if vector_store_id:
            # Usa il vector store esistente
            self.vector_store_id = vector_store_id
        else:
            # Crea un nuovo Vector Store se non fornito
            vector_store = self.client.beta.vector_stores.create(name="Document Archive")
            self.vector_store_id = vector_store.id
            print(f"New vector store created: {vector_store_id}")
            

        # Aggiornare l'assistente per usare il Vector Store
        self.client.beta.assistants.update(
            assistant_id=self.assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [self.vector_store_id]}},
        )

    def create_thread(self):
        self.thread = self.client.beta.threads.create(
            messages=[{"role": "assistant", "content": "Sei un assistente utile ed intelligente che estrae informazioni da documenti dati"}]
        )

    def continue_thread(self, new_message):
        # Invia un nuovo messaggio
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=new_message
        )

        # Esegui il run del thread e attendi la risposta completa
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id, assistant_id=self.assistant.id
        )

        # Estrai il contenuto del messaggio finale
        messages = list(self.client.beta.threads.messages.list(thread_id=self.thread.id, run_id=run.id))
        if messages:
            assert messages[0].content[0].type == "text"
            final_message = messages[0].content[0].text
            return final_message
        else:
            return "No response available."
