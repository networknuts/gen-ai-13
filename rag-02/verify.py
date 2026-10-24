import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

job_id = input("Enter Job ID: ")

answer = redis_client.get(job_id)
print(answer)