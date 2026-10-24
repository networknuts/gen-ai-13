import uuid 
import redis 

# SETUP THE REDIS CONNECTION
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# GENERATE PAYLOAD AND UPLOAD TO REDIS
def upload_payload(query):
    job_id = str(uuid.uuid4())
    payload = {
        "job_id": job_id,
        "query": query
    }
    queue_name = "rag:requests"
    redis_client.rpush(queue_name,str(payload))
    return job_id

query = input("Enter your query: ")
job = upload_payload(query)
print(f"Job ID: {job}")
print("QUERY SENT SUCCESSFULLY TO QUEUE")