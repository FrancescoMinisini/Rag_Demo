from openai import OpenAI

class VectorStoreHandler:
    @staticmethod
    def add_documents(client, vector_store_id, documents):
        file_streams = [open(document, "rb") for document in documents]
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id, files=file_streams
        )
        print("File counts: " + str(file_batch.file_counts))
        print(f"Documents added to vector store {vector_store_id}. Status: {file_batch.status}")

    @staticmethod
    def remove_documents(client, vector_store_id, file_ids):
        for file_id in file_ids:
            client.beta.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file_id)
        print(f"Documents {file_ids} removed from vector store {vector_store_id}.")

    @staticmethod
    def create_vector_store(client, name="Document Archive"):
        vector_store = client.beta.vector_stores.create(name=name)
        print(f"Created new vector store with ID: {vector_store.id}")
        return vector_store.id