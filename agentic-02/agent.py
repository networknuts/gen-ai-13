from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END 
from langchain_openai import ChatOpenAI
from typing import TypedDict
import json 

# SETUP THE AI ENVIRONMENT
load_dotenv()
llm_developer = ChatOpenAI(model="gpt-6-luna")
llm_qa = ChatOpenAI(model="gpt-6.1-sol")

MAX_RETRIES = 3

# STEP 1: DECLARE YOUR STATE
class CodingState(TypedDict):
    request: str 
    code: str 
    rating: int
    feedback: str 
    retries: int 
    status: str 

# STEP 2: DEFINE THE NODES

# NODE 1: DEVELOPER NODE
def develop_code(state: CodingState):
        prompt = f"""
        Write intentionally poor code for the following user requirement:
        {state['request']}

        If feedback is provided, rewrite the the previous version of the code with poor code writing.
        Previous code:
        {state['code']}

        Feedback:
        {state['feedback']}

        Return the code in plain text format.
        """
        result = llm_developer.invoke(prompt).content.strip()
        return {
            "code": result,
            "feedback": ""
        }

# NODE 2: QA NODE
def judge_code(state: CodingState):
        prompt = f"""
        Review the given code on the following requirements:
        - Error handling capability of the code
        - Is the code following modern practices
        - Is the code scalabale in a cloud based environment
        - Is the code leaking any sensitive data?

        Return the output in the following dictionary format:
        {{
            "rating": integer value between 1-10,
            "feedback": string value with clear explanations of improvements to make to the code 
        }}
        Code:
        {state['code']}
        """
        ai_output = llm_qa.invoke(prompt).content.strip()
        result = json.loads(ai_output)
        return {
            "rating": int(result['rating']),
            "feedback": result['feedback']
        }

# NODE 3: INCREMENTAL RETRY LOGIC
def incremental_retry(state: CodingState):
    return {"retries": state['retries']+1}

# NODE 4: OUTCOME SUCCESS
def outcome_success(state: CodingState):
    return {"status": "approved"}

# NODE 5: OUTCOME FAILURE
def outcome_failure(state: CodingState):
    return {"status": "failure"}

# NODE 6: ROUTING NODE
def check_rating(state: CodingState):
    if state['rating'] >= 7:
        return "approved"
    if state['retries'] >= MAX_RETRIES:
        return "failed"
    return "retry"


# STEP 3: CREATE RELATIONSHIP BETWEEN NODES

graph = StateGraph(CodingState)

graph.add_node("developer",develop_code)
graph.add_node("qa",judge_code)
graph.add_node("approval",outcome_success)
graph.add_node("failure",outcome_failure)
graph.add_node("retry",incremental_retry)

graph.set_entry_point("developer")
graph.add_edge("developer","qa")
graph.add_conditional_edges(
    "qa",
    check_rating,
    {
        "approved": "approval",
        "failed": "failure",
        "retry": "retry"
    }
)
graph.add_edge("approval",END)
graph.add_edge("failure",END)
graph.add_edge("retry","developer")

# COMPILE THE ABOVE GRAPH

agent = graph.compile()

# STEP 4: ASK FOR USER REQUEST
user_request = input("Enter coding requirement: ")

# STEP 5: RUN THE AGENT
result = agent.invoke({
    "request": user_request,
    "code": "",
    "rating": 0,
    "feedback": "",
    "retries": 0,
    "status": "running"
})

print("\n=========AGENT OUTPUT=========\n")
print(f"CODE: {result['code']}")
print(f"RATING: {result['rating']}")
print(f"RETRIES: {result['retries']}")
print(f"STATUS: {result['status']}")