from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5.1", temperature=0.1)

class GradeHallucinations(BaseModel):
    """
    Binary score for hallucination present in generated answer.
    """
    binary_score: bool = Field(
        description="Answer is grounded in the facts, True or False"
    )

structured_llm_grader = llm.with_structured_output(GradeHallucinations)

system_prompt = """
You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. 
Give a binary score True or False. True means that the answer is grounded in / supported by the set of facts.
"""

hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', system_prompt),
        ('human', "Set of facts: {facts} \nGenerated answer: {answer}")
    ]
)

hallucination_grader = hallucination_prompt | structured_llm_grader