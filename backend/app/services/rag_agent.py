from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os
from app.utils.elasticsearch import search_documents
from dotenv import load_dotenv

load_dotenv()

# ✅ Load Gemini API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY is not set!")
else:
    print(f"✅ Google API Key loaded: {api_key[:5]}***")

def get_answer_from_documents(query):
    try:
        print(f"\n🔍 Incoming query: {query}")

        # Step 1: Search Elasticsearch
        docs = search_documents(query)
        print(f"📄 Retrieved {len(docs)} documents from Elasticsearch")

        if not docs:
            return "No documents found for the query."

        documents = [Document(page_content=d) for d in docs]

        # Step 2: Split documents
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)
        print(f"🧩 Split into {len(chunks)} chunks")

        # ✅ Step 3: Use embeddings model correctly
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",  # ✅ Set explicitly
            google_api_key=api_key
        )

        vectorstore = FAISS.from_documents(chunks, embeddings)

        # ✅ Step 4: Use Gemini 2.0 Flash properly
        qa = RetrievalQA.from_chain_type(
            llm=ChatGoogleGenerativeAI(
                model="models/gemini-2.0-flash-001",  # ✅ Explicit model name
                google_api_key=api_key
            ),
            retriever=vectorstore.as_retriever()
        )

        # Step 5: Ask LLM
        result = qa.run(query)
        print(f"🤖 Gemini Answer: {result}")

        return result

    except Exception as e:
        print(f"❌ Error in RAG pipeline: {e}")
        return "An error occurred while processing the query."
