from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5.1", temperature=0.1)

class GradeAnswer(BaseModel):
    binary_score: bool = Field(
        description="Does the generation address the question? True or False"
    )

structured_llm_grader = llm.with_structured_output(GradeAnswer)

system_prompt = """
You are a grader assessing whether an answer addresses / resolves a question.
Give a binary score True or False. True means the answer addresses the question.
"""

answer_grader_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', system_prompt),
        ('human', "User question: {question} \nLLM generation: {generation}")
    ]
)

answer_grader = answer_grader_prompt | structured_llm_grader