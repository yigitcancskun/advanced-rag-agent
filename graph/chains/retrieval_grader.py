from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import sys
import os 
load_dotenv()


# Add parent directory to path to import ingestion
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ingestion import retriever

llm = ChatOpenAI(model="gpt-5.1", temperature=0)

class GradeDocuments(BaseModel):
    """
    Binary score for relevance check on retrieved documents.
    """

    binary_score : str = Field(
        description = "Binary score for relevance check on retrieved documents, 'yes' or 'no' "

    )

structured_llm_grader = llm.with_structured_output(GradeDocuments)

system_prompt = """
You are a grader assesing whether an LLM generation is grounded in / supported by a set of retrieved facts. 
If the document contains keyword or semantic meaning related t question, grade it as relevant.
Give a binary score 'yes' or 'no'.'Yes' means that answer is grounded in / supported by the set of facts.
"""

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', system_prompt),
        ('human', "Retrieved document: {document} User question : {question}")
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader