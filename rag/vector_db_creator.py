import os
import azure.functions as func
import logging
import config
from langchain_community.document_loaders import AzureBlobStorageFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from azure.identity import DefaultAzureCredential
from azure.storage.blob import  ContainerClient   
from langchain_core.documents import Document

def create_vector_store():
    try:
        logging.info('Python HTTP trigger function processed a request.')

        connection_string = "BlobEndpoint=https://paymentsdatasaket.blob.core.windows.net/;QueueEndpoint=https://paymentsdatasaket.queue.core.windows.net/;FileEndpoint=https://paymentsdatasaket.file.core.windows.net/;TableEndpoint=https://paymentsdatasaket.table.core.windows.net/;SharedAccessSignature=sv=2024-11-04&ss=bfqt&srt=co&sp=rwdlacupiytfx&se=2025-07-15T18:03:25Z&st=2025-07-15T09:48:25Z&spr=https&sig=7bhLO7SF2f%2FzRCChFNInROzSppodjhRt%2F6%2F5pqxnL9s%3D"
        container_name = "paymentdata"
        blob_name_rp = "refund_policy.txt"  # optional: only load files from this prefix
        blob_name_tos = "terms_of_service.txt"
        blob_faq = "user_faqs.txt"

        container = ContainerClient.from_connection_string( connection_string, container_name )  
        blob_client_rp = container.get_blob_client(blob_name_rp)

        rp_text = blob_client_rp.download_blob(encoding="utf-8").readall()
        tos_text = container.get_blob_client(blob_name_tos).download_blob(encoding="utf-8").readall()
        faq_text = container.get_blob_client(blob_faq).download_blob(encoding="utf-8").readall()

        all_text = rp_text + "\n" + tos_text + "\n" + faq_text
        doc = Document(page_content=all_text, metadata={"source": "refund_policy.txt"})
        docs = [doc]
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        if not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] =  config.OPENAI_KEY
        
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        vector_store = FAISS.from_documents(chunks, embeddings)

        vector_store.save_local(os.getcwd(), "embeddings")


        with open("embeddings.faiss", "rb") as f:
            container.upload_blob(name="embeddings.faiss", data = f, overwrite=True)


        with open("embeddings.pkl", "rb") as f:
            container.upload_blob(name="embeddings.pkl", data = f, overwrite=True)


    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # This block always executes
        print("Execution complete.")
