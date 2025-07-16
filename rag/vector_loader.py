# Code to create/load vector store
# Code to load and split documents
import os
import config
from langchain_community.document_loaders import AzureBlobStorageFileLoader
from azure.storage.blob import  ContainerClient   
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
def get_vector_store():
    try:
        """
        loader = AzureBlobStorageFileLoader(
        conn_str="BlobEndpoint=https://paymentsdatasaket.blob.core.windows.net/;QueueEndpoint=https://paymentsdatasaket.queue.core.windows.net/;FileEndpoint=https://paymentsdatasaket.file.core.windows.net/;TableEndpoint=https://paymentsdatasaket.table.core.windows.net/;SharedAccessSignature=sv=2024-11-04&ss=bf&srt=o&sp=rwdlaciytfx&se=2025-07-14T19:37:43Z&st=2025-07-14T11:37:43Z&spr=https&sig=FbUhAxh8obkHm6BfEFFYhaj5LH9kzoyrDipQBZeP7%2B8%3D",
        container="paymentdata",
        blob_name="refund_tos_embeddings")
        """
        connection_string = "BlobEndpoint=https://paymentsdatasaket.blob.core.windows.net/;QueueEndpoint=https://paymentsdatasaket.queue.core.windows.net/;FileEndpoint=https://paymentsdatasaket.file.core.windows.net/;TableEndpoint=https://paymentsdatasaket.table.core.windows.net/;SharedAccessSignature=sv=2024-11-04&ss=bf&srt=co&sp=rwdlaciytfx&se=2025-07-16T21:30:25Z&st=2025-07-16T13:15:25Z&spr=https,http&sig=zi4oQkXicleRj2LKyZQLIVyandzp0YdvdK5oVMr%2FW88%3D"
        container_name = "paymentdata"
        blob_name_embeddings = "embeddings.faiss"  # optional: only load files from this prefix
        blob_name_pkl = "embeddings.pkl"  # optional: only load files from this prefix

        container = ContainerClient.from_connection_string( connection_string, container_name )  
        blob_client = container.get_blob_client(blob_name_embeddings)

        with open("embeddings.faiss", "wb") as f:
            blob_data = blob_client.download_blob()
            f.write(blob_data.readall())

        blob_client = container.get_blob_client(blob_name_pkl)

        with open("embeddings.pkl", "wb") as f:
            blob_data = blob_client.download_blob()
            f.write(blob_data.readall())

        if not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] =  config.OPENAI_KEY

        embeddings2 = OpenAIEmbeddings(model="text-embedding-3-large")
        vector_store = FAISS.load_local(
            os.getcwd(),
            embeddings=embeddings2,
            index_name="embeddings",
            allow_dangerous_deserialization=True
        )


        return vector_store
    
    except Exception as e:
        raise Exception("Error in loading vector DB")

