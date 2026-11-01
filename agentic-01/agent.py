from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END 
from langchain_openai import ChatOpenAI
from typing import TypedDict

# SETUP THE AI ENVIRONMENT
load_dotenv()
llm = ChatOpenAI(model="gpt-5.6-luna")

# STEP 1: DECLARE YOUR STATE
class CodingState(TypedDict):
    request: str 
    code: str 
    rating: int 

# STEP 2: DEFINE THE NODES

# NODE 1: DEVELOPER NODE
def develop_code(state: CodingState):
    response = llm.invoke(
        f"""
        Write code for the following user requirement:
        {state['request']}

        Return the code in plain text format.
        """
    )
    return {
        "code": response.content 
    }

# NODE 2: QA NODE
def judge_code(state: CodingState):
    response = llm.invoke(
        f"""
        Review the given code on the following requirements:
        - Error handling capability of the code
        - Is the code following modern practices
        - Is the code scalabale in a cloud based environment
        - Is the code leaking any sensitive data?

        Provide a single rating between 1-10 after judging the code on the above requirements.

        Code:
        {state['code']}
        """
    )
    return {
        "rating": response.content 
    }

# STEP 3: CREATE RELATIONSHIP BETWEEN NODES

graph = StateGraph(CodingState)

graph.add_node("developer",develop_code)
graph.add_node("qa",judge_code)

graph.add_edge(START,"developer")
graph.add_edge("developer","qa")
graph.add_edge("qa",END)

# COMPILE THE ABOVE GRAPH

agent = graph.compile()

# STEP 4: ASK FOR USER REQUEST
user_request = input("Enter coding requirement: ")

# STEP 5: RUN THE AGENT
result = agent.invoke({
    "request": user_request,
    "code": "",
    "rating": ""
})

print("\n=========AGENT OUTPUT=========\n")
print(f"RATING: {result['rating']}")
print(f"CODE: {result['code']}")