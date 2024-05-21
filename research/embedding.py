from sentence_transformers import SentenceTransformer
from transformers import pipeline
import chromadb

# Sample documents
documents = [
    "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
    "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
    "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
    "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
    "Llamas are vegetarians and have very efficient digestive systems",
    "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
]

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection = client.create_collection(name="docs")

# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Store each document in a vector embedding database
for i, d in enumerate(documents):
    embedding = embedder.encode(d).tolist()  # Convert numpy array to list
    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[d]
    )

# An example prompt
prompt = "What animals are llamas related to?"

# Generate an embedding for the prompt and retrieve the most relevant doc
prompt_embedding = embedder.encode(prompt).tolist()  # Convert numpy array to list
results = collection.query(
    query_embeddings=[prompt_embedding],
    n_results=1
)
data = results['documents'][0][0]

print(data)