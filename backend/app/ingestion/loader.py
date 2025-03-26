from langchain.chat_models import init_chat_model
from langchain_google_vertexai import VertexAIEmbeddings
import bs4
from langchain_community.document_loaders import WebBaseLoader
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
import time

# Load variables from .env
load_dotenv()

# Access your keys
pinecone_api_key = os.getenv("PINECONE_API_KEY")
# google_api_key = os.getenv("GOOGLE_API_KEY")


# Set up Vertex AI model
# llm = init_chat_model("gemini-2.0-flash-001", model_provider="google_vertexai")

# Embedding model
# embeddings = VertexAIEmbeddings(model="text-embedding-004")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)

index_name = "quickstart"

# pc.create_index(
#     name=index_name,
#     dimension=1024,  # Replace with your model dimensions
#     metric="cosine",  # Replace with your model metric
#     spec=ServerlessSpec(
#         cloud="aws",
#         region="us-east-1"
#     )
# )

# data = [
#     {"id": "vec1", "text": "Apple is a popular fruit known for its sweetness and crisp texture."},
#     {"id": "vec2", "text": "The tech company Apple is known for its innovative products like the iPhone."},
#     {"id": "vec3", "text": "Many people enjoy eating apples as a healthy snack."},
#     {"id": "vec4", "text": "Apple Inc. has revolutionized the tech industry with its sleek designs and user-friendly interfaces."},
#     {"id": "vec5", "text": "An apple a day keeps the doctor away, as the saying goes."},
#     {"id": "vec6", "text": "Apple Computer Company was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne as a partnership."}
# ]

# embeddings = pc.inference.embed(
#     model="multilingual-e5-large",
#     inputs=[d['text'] for d in data],
#     parameters={"input_type": "passage", "truncate": "END"}
# )
# print(embeddings[0])

# # Wait for the index to be ready
# while not pc.describe_index(index_name).status['ready']:
#     time.sleep(1)

index = pc.Index(index_name)

# vectors = []
# for d, e in zip(data, embeddings):
#     vectors.append({
#         "id": d['id'],
#         "values": e['values'],
#         "metadata": {'text': d['text']}
#     })

# index.upsert(
#     vectors=vectors,
#     namespace="ns1"
# )

# print(index.describe_index_stats())


query = "Tell me about the tech company known as Apple."

embedding = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[query],
    parameters={
        "input_type": "query"
    }
)

results = index.query(
    namespace="ns1",
    vector=embedding[0].values,
    top_k=3,
    include_values=False,
    include_metadata=True
)

print(results)
