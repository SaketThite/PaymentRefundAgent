# PaymentRefundAgent
This is a sample project t demonstrate How Open AI capabilities can be used to determine a core piece of business process on an ecommerce website.
This project asks the user for a Transaction Id, looks up transaction details in DB, uses a vector representation of the refund policy and passes thee parametres to an Open AI model so it can determine if the refund can be processed or not.

The project is made up of the following components
a. A transaction database, which records payment transactions across different merchants. This includes standard details like, Transaction date, Amount, Status, Refund Status etc. The data\MockGenerator.py file generates 15K dummy records in a Json file. I have used Azure Data Factory to import them into an Azure SQl database


b. Text files which constitute the refund policy of this ecommerce website. For simplicity, we have consodered a single policy for all merchants. The files which constitute the refund policy are stored in Aure Blob Storage.


c. Vector DB - a vector representation of the refund policies. This is generated using the FAISS library against the Open AI embedding model" text-embedding-3-large". The Vector DB is also stored in Azure blob storage as a binary file. The file Rag\vector_db_creater has the cide to generate the embeddings and store them into Azure Blob Storage. The file vector_loader is used by the agent to download the vectors and load them into memory


d. Tools: Two tools are used, 1. tools\transaction_tools.py, which loads the transaction details for a given transaction id, and 2. Inline lambda funciton which queries the vector store and fetches k similar records.



The Actual Agent: This brings together all the above elements, defines a tools arrray woth the 2 tools, mentioned above, Creates an object to wrk with Open AI model "gpt-4o", defines a suitable prompt for the LLM to understand what steps it needs to take to determine if a refund is valid, and calls into the LLM to get the result.
