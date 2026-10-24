from dotenv import load_dotenv
from openai import OpenAI 
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import redis 
import ast 

# SETUP THE AI ENVIRONMENT
load_dotenv()
client = OpenAI()

EMBEDDING_MODEL = "text-embedding-3-large"
QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION_NAME = "example_collection"

embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL
)

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=QDRANT_COLLECTION_NAME,
    url=QDRANT_URL,
)

# SETUP THE REDIS ENVIRONMENT
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
queue_name = "rag:requests"

print("WORKER STARTED, WAITING FOR REQUESTS.")

while True:
    queue_name, raw_payload = redis_client.blpop(queue_name)
    payload = ast.literal_eval(raw_payload)
    job_id = payload["job_id"]
    query = payload["query"]
    print(f"Processing Query: {job_id}")
    # AI RAG CODE - RETRIEVAL LOGIC
    search_results = qdrant.similarity_search(query)
    context = []
    for chunk in search_results:
        chunk_block = f"""
        Page Content:
        {chunk.page_content}
        Page Number:
        {chunk.metadata.get('page','N/A')}
        """
        context.append(chunk_block)
    SYSTEM_PROMPT = f"""
You are an AI RAG Assistant.
You have been provided content extracted from PDF document(s).

Each section includes:
- Page Content
- Page Number

Answer the user's question using only this provided information.
If the answer is available:
- Respond from the data you have
- Mention the relevant page number(s) from where the data came from

If the answer is not available:
- State to the user that answer is not available in your knowledge base

Data:
{context}
"""
    response = client.responses.create(
        model="gpt-5.6-luna",
        input=query,
        instructions=SYSTEM_PROMPT
    )
    answer = response.output_text
    redis_client.set(str(job_id),answer,ex=86400)
    print(f"Job ID: {job_id} processed successfully!")