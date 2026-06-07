# RAG imports
import os
from openai import OpenAI
from pinecone.grpc import PineconeGRPC as Pinecone
from tenacity import retry, wait_exponential, stop_after_attempt
from dotenv import load_dotenv

load_dotenv()


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

# Following Pinecones semantic search docs next steps are to query with the vector and top_k
# therefore, set include_metadata=True to get the stored chunk text back
# include_values=False is a better integration for performance when not needing raw vector values
def retrieve_top_k(query: str, top_k: int = 5, namespace: str = "__default__"):
    query_vec = get_embedding(query)

    results = index.query(
        namespace=namespace,
        vector=query_vec,
        top_k=top_k,
        include_metadata=True,
        include_values=False,
    )
    return results.matches

# The same exponential back off strategy for llm call is used for retrieving 
# top k to query all expected results into a vector query if all results are true 
# it'll return all matches
@retry(
        wait=wait_exponential(multiplier=1, min=2, max=60),
        stop=stop_after_attempt(5)
)

def retrieve_top_k_retries(
    query: str,
    top_k: int = 5,
    namespace: str = "__default__"
):
    
    query_vec = get_embedding(query)

    results = index.query(
        namespace=namespace,
        vector=query_vec,
        top_k=top_k,
        include_metadata=True,
        include_values=False,
    )
    return results.matches

# Inject retrieved text into the system, take the top matches, pull chunk_text from metadata, and build a context block.
# This particular part is what is passed to the LLM
def build_context(matches) -> str:
    chunks = []
    for i in matches:
        meta = i.metadata or {}
        text = meta.get("chunk_text", "")
        if text:
            chunks.append(text)
    return "\n\n---\n\n".join(chunks)

# Per OpenAIs embeddings docs, we are now splitting the corpus into chunks smaller than the model token limit
# embed each chunk, and store those embeddings in a vector database
# The embeddings create the endpoint and to allow the input to stay within the models token limit
def upsert_chunks(chunks: list[dict], namespace: str = "__default__"):
    vectors = []
    for chunk in chunks:
        emb = get_embedding(chunk["text"])
        vectors.append({
            "id": chunk["id"],
            "values": emb,
            "metadata":{
                "doc_id": chunk["doc_id"],
                "chunk_index": chunk["chunk_index"],
                "source": chunk["source"],
                "chunk_text": chunk["text"],
            }
        })
    index.upsert(vectors=vectors, namespace=namespace)
