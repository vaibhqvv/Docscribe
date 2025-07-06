import os
from pathlib import Path
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

PERSIST_DIR="./chroma_store"
UPLOAD_DIR="./uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_vectorstore(uploaded_files):
    # embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    file_paths = []

    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR)/file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    docs = []
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_documents(docs)

    # texts = [chunk.page_content for chunk in chunks]
    # metadatas = [chunk.metadata for chunk in chunks]
    # ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]
    
    embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L12-v2")
    

    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
        vectorstore.add_documents(texts)
        vectorstore.persist()
    else:
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            persist_directory=PERSIST_DIR
        )
        vectorstore.persist()
        
    return vectorstore.as_retriever()

        
