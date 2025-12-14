from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

class RouteQuery(BaseModel):
    """
    Route a user query to the most relevant datasource
    """

    datasource : Literal["vectorstore","websearch"] = Field(
        ...,
        description = "Given a user question choose to route it to web search or a vectorstore"
    ) 

llm = ChatOpenAI(model="gpt-5.1", temperature=0)
structured_llm_router = llm.with_structured_output(RouteQuery)

system_prompt = """
You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains information about AI agents and websearch returns relevant webpages.
Use the vectorstore for questions on these topics. For all else, use web-search.
"""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{question}")
    ]
)


question_router = route_prompt | structured_llm_router

if __name__ == "__main__":
    print(question_router.invoke(
        {"question": "What is the best AI agent for customer support?"}
    ))