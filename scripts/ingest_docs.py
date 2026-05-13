import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader

def ingest_docs():
    print("🚀 Starting document ingestion into ChromaDB...")
    
    # 1. Load documents from data/docs/
    loader = DirectoryLoader('data/docs', glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    print(f"📄 Loaded {len(documents)} documents.")
    
    # 2. Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✂️ Split documents into {len(chunks)} chunks.")
    
    # 3. Initialize embeddings model
    # Using the one specified in the guide: sentence-transformers/all-MiniLM-L6-v2
    print("🧠 Initializing embeddings model (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 4. Create and persist ChromaDB
    print("📦 Creating persistent ChromaDB collection in data/chromadb/...")
    persist_directory = 'data/chromadb'
    
    # Clean up existing db if it exists
    if os.path.exists(persist_directory):
        import shutil
        # Note: In a production app, you might want to update instead of delete.
        # But for a seed script, starting fresh is often safer.
        # However, Chroma handles persistence well. Let's just load it.
        pass

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    # In newer versions of Chroma/LangChain, persistence is handled automatically 
    # or via the constructor. We'll just confirm with a test query.
    print("✅ Ingestion complete.")
    
    # 5. Verify with a test query
    print("\n🔍 Running test query: 'how do I return an item?'")
    results = vectordb.similarity_search("how do I return an item?", k=2)
    
    for i, res in enumerate(results):
        print(f"\nResult {i+1} from {res.metadata.get('source')}:")
        print(f"{res.page_content[:200]}...")

if __name__ == "__main__":
    ingest_docs()
