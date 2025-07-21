from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA

def create_llm_agent(json_path: str):
    loader = JSONLoader(file_path=json_path, jq_schema='.', text_content=False)
    docs = loader.load()
    db = FAISS.from_documents(docs, OpenAIEmbeddings())
    qa_chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=db.as_retriever())
    return qa_chain