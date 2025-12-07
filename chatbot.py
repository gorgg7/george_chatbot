from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def get_knowledge_base(path="Grag"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    kb = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    return kb

def rag_chat_bot(api_key, question, history=None):
    prompt = f"""
    you are reader expert get all information that user need
    VERY IMPORTANT:
        - Respond in the same language as the user's question.
    """
    knowledge_base = get_knowledge_base("Grag")
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        model="openai/gpt-oss-20b:free",
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=knowledge_base.as_retriever()
    )

    if history:
        history_context = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])
        query_with_context = f"{history_context}\n\nUser: {question}"
    else:
        query_with_context = question
    result = qa.run(query_with_context)
    print(result)
    return result