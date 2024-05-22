from sentence_transformers import SentenceTransformer
import chromadb
import hashlib
import time

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection = client.create_collection(name="docs")

# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Function to add a document with a timestamp
def add_document(document: str):
    # Generate an embedding for the document
    embedding = embedder.encode(document).tolist()  # Convert numpy array to list
    
    # Create a unique ID for the document using a hash of its content
    document_id = hashlib.md5(document.encode()).hexdigest()
    
    # Add the document to the collection with the current timestamp
    collection.add(
        ids=[document_id],
        embeddings=[embedding],
        documents=[document],
        metadatas=[{'timestamp': time.time()}]  # Store the current timestamp
    )

# Function to search for documents
def search(prompt: str, n_results: int = 1):
    # Generate an embedding for the prompt
    prompt_embedding = embedder.encode(prompt).tolist()  # Convert numpy array to list
    
    # Query the collection for the most relevant documents
    results = collection.query(
        query_embeddings=[prompt_embedding],
        n_results=n_results
    )
    
    return results['documents'][0]

# Function to delete documents older than a given age (in seconds)
def delete_old_documents(max_age: int):
    current_time = time.time()
    all_documents = collection.get()  # Retrieve all documents in the collection
    
    for doc_id, metadata in zip(all_documents['ids'], all_documents['metadatas']):
        if current_time - metadata['timestamp'] > max_age:
            collection.delete(ids=[doc_id])

# Sample documents
documents = [
    "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
    "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
    "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
    "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
    "Llamas are vegetarians and have very efficient digestive systems",
    "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
    "Mic loves dank memes but his 15 year old says that he does them wrong",
]

# Add each document to the collection
for doc in documents:
    add_document(doc)

# An example prompt
prompt = "What animals are llamas related to?"

# Search for the most relevant document
results = search(prompt)
print(results)


# An example prompt
prompt = "So many dank memes"

# Search for the most relevant document
results = search(prompt)
print("dank", type(results))
print("dank", str(results))

prompt = "432432 { tx: 22 }"
results = search(prompt)
print("tx", str(results))


# Delete documents older than a given age (e.g., 24 hours)
delete_old_documents(max_age=24*60*60)
