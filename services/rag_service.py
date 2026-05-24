# RAG imports
import os
from openai import OpenAI
from pinecone.grpc import PinconeGRPC as Pinecone


# Environment variable handling
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(host=os.getenv("PINECONE_INDEX_HOST"))

EMBED_MODEL = "text-embedding-3-small"

# First step to live retrieval / consult OpenAIs embeddings guide (https://developers.openai.com/api/docs/guides/embeddings) which shows the same
# pattern for a query call `client.embeddings.create()` and use the returned vector
def get_embedding(text:str) -> list[float]:
    text = text.replace("\n", " ")
    response = openai_client.embeddings.create(
        model=EMBED_MODEL,
        input=text,
        encoding_format="float",
    )
    return response.data[0].embedding