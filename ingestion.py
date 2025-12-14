from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

urls = ["https://nurettinalabay.com.tr/yapay-zeka-ajanlari/"]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,
    chunk_overlap=200,
)
splits = text_splitter.split_documents(docs_list)

vectorstore = Chroma.from_documents(
    documents = splits,
    collection_name = "ai-agents",
    embedding = OpenAIEmbeddings(),
    persist_directory = "./chroma_db"
)

retriever = vectorstore.as_retriever()




if __name__ == "__main__":
    print(docs_list)