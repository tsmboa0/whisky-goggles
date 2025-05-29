import os
from typing import Annotated, Dict
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph

from app.utils.prompt import mediator_system_prompt
from dotenv import load_dotenv
from app.core.matcher import WhiskyMatcher
import ast
import re

response_format = {
    "name": "Whisky Bottle Name with the year and age (as it is called in a liquor store). You can ignore the year if it is not present in the OCR text.",
    "score": "Confidence score of the whisky bottle"
}

load_dotenv()

# load the matcher
matcher = WhiskyMatcher()

# currently using deepseek-r1-distill-llama-70b or llama-3.3-70b-versatile
LLM = init_chat_model(model= os.getenv("MODEL_NAME"), model_provider=os.getenv("MODEL_PROVIDER"))

# Add a custom reducer
def replaceString(left:str, right:str)->str:
    return right

def replaceList(left:list, right:list)->list:
    return right

class State(TypedDict):
    messages: Annotated[list, add_messages]
    clip_result: Annotated[str, replaceString]
    vision_result:Annotated[str, replaceString]
    final_result: Annotated[list, replaceList]

def Mediator(state: State):
    messages= state['messages']
    vision_result = state["vision_result"]
    clip_result = state["clip_result"]

    prompt = ChatPromptTemplate.from_template(mediator_system_prompt)

    system_message = prompt.invoke({
        "clip_result": clip_result,
        "vision_result": vision_result,
        "response_format": response_format
    }).to_messages()

    result = LLM.invoke(system_message+messages)

    cleaned_result = extract_dict_from_response(result.content)

    matched_bottles = TextSimilaritySearch(cleaned_result)

    return {"final_result": matched_bottles}


def TextSimilaritySearch(data:Dict):
    bottle_name = data['name']
    confidence_score = data['score']

    matched_bottles = matcher.match_text(bottle_name)
    matched_bottles[0]['confidence_score'] = confidence_score

    return matched_bottles

def extract_dict_from_response(response: str):
    # Find the first {...} block using regex
    match = re.search(r"\{.*?\}", response, re.DOTALL)
    if not match:
        raise ValueError("No dictionary found in the response.")

    dict_str = match.group(0)
    try:
        parsed = ast.literal_eval(dict_str)
        return parsed  # parsed is a dict
    except Exception as e:
        raise ValueError(f"Failed to parse dict: {e}")
    



builder = StateGraph(State)
builder.add_node("mediator", Mediator)
builder.add_edge(START, "mediator")
builder.add_edge("mediator", END)

graph = builder.compile()