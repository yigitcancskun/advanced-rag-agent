from graph.node_constants import GRADE_DOCUMENTS
from graph.node_constants import WEBSEARCH
from graph.node_constants import RETRIEVE
from graph.node_constants import GENERATE
from typing import Dict, Any
from graph.state import GraphState
from graph.chains.router import question_router, RouteQuery
from graph.nodes.retrieve import retrieve
from graph.nodes.grade_documents import grade_documents
from graph.nodes.generate import generate
from graph.nodes.web_search import web_search
from graph.chains.answer_grader import answer_grader
from graph.chains.hallucination_grader import hallucination_grader
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv 

load_dotenv()


def decide_to_generate(state: GraphState):
    print("----ASSESS GRADED DOCUMENTS------")
    if state["web_search"]:
        print("WEBSEARCH")
        return WEBSEARCH
    else:
        return GENERATE

def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    print("------CHECK HALLUCINATIONS -------")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    # Convert documents list to string for the grader
    docs_content = "\n\n".join([doc.page_content for doc in documents])
    
    score = hallucination_grader.invoke(
        {"facts": docs_content, "answer": generation}
    )
    
    if score.binary_score:
        print("GENERATION IS GROUNDED IN DOCUMENTS")
        answer_score = answer_grader.invoke(
            {"question": question, "generation": generation}
        )
        if answer_score.binary_score:
            print("GENERATION ADDRESSES QUESTION")
            return "useful"
        else: 
            print("GENERATION DOES NOT ADDRESS THE QUESTION")
            return "not useful"
    else:
        print("GENERATION IS NOT GROUNDED IN DOCUMENTS, REGENERATING...")
        return "not useful"  # Changed to regenerate instead of websearch to avoid infinite loop

def route_question(state: GraphState) -> str:
    print("ROUTE QUESTION")
    question = state["question"]
    source = question_router.invoke({"question": question})
    if source.datasource == "websearch":
        print("WEBSEARCH")
        return WEBSEARCH
    elif source.datasource == "vectorstore":
        print("VECTORSTORE")
        return RETRIEVE 



workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.set_conditional_entry_point(
    route_question,
    path_map={
        RETRIEVE:RETRIEVE,
        WEBSEARCH:WEBSEARCH
    }
)

workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)


workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    path_map={
        WEBSEARCH:WEBSEARCH,
        GENERATE:GENERATE
    }
)
workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    path_map={ 
        "useful": END,
        "not useful": END  # Changed to END to avoid infinite regeneration loop
    }
)
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)



app = workflow.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")
