import os
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import AIMessage
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph

from app.utils.prompt import mediator_system_prompt
from app.utils.logger import logger
from dotenv import load_dotenv
from app.core.matcher import WhiskyMatcher
from app.config import MODEL_NAME, MODEL_PROVIDER


load_dotenv()

# load the matcher
matcher = WhiskyMatcher()

# currently using deepseek-r1-distill-llama-70b or llama-3.3-70b-versatile
LLM = init_chat_model(model= MODEL_NAME, model_provider=MODEL_PROVIDER)

# Add a custom reducer
def replaceString(left:str, right:str)->str:
    return right

def replaceList(left:list, right:list)->list:
    return right

class State(TypedDict):
    messages: Annotated[list, add_messages]
    clip_result: Annotated[str, replaceString]
    ocr_result:Annotated[str, replaceString]
    final_result: Annotated[list, replaceList]

def Mediator(state: State):
    messages= state['messages']
    ocr_result = state["ocr_result"]
    clip_result = state["clip_result"]

    prompt = ChatPromptTemplate.from_template(mediator_system_prompt)

    system_message = prompt.invoke({
        "clip_result": clip_result,
        "ocr_result": ocr_result
    }).to_messages()

    result = LLM.invoke(system_message+messages)

    return {"messages": [result]}


def TextSimilaritySearch(state:State):
    messages = state['messages']

    # Retrive the content of the Mediators answer
    lastMessage : AIMessage = messages[len(messages)-1]
    full_text = lastMessage.content.split("name:")
    bottle_name = full_text[1].split("score:")[0]

    logger.info("The mediator result is: ",full_text[1])

    confidence_score = full_text[1].split("score:")[1]

    matched_bottles = matcher.match_text(bottle_name)
    matched_bottles[0]['confidence_score'] = confidence_score

    return {"final_result": matched_bottles}

builder = StateGraph(State)
builder.add_node("mediator", Mediator)
builder.add_node("search", TextSimilaritySearch)
builder.add_edge(START, "mediator")
builder.add_edge("mediator", "search")
builder.add_edge("search", END)

graph = builder.compile()