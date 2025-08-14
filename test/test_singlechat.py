import sys
from pathlib import Path
from langchain_community.vectorstores import FAISS
from document_portal.src.single_document_chat.data_ingestion import SingleDocumentChatDataIngestion
from document_portal.src.single_document_chat.retrieval import ConversationalRag
from document_portal.utils.model_loader import ModelLoader
# from document_portal

FAISS_INDEX_PATH = Path("faiss_index")

def test_conversational_rag():
    try:
        model_loader = ModelLoader()
        
        if FAISS_INDEX_PATH.exists():
            embeddings = model_loader.load_embeddings()
            vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
            retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        else:
            print("faiss_index does not exist. Please run data ingestion first.")
            with open("pdf_path", "rb") as f:
                upload_files = [f]
            data_ingestion = SingleDocumentChatDataIngestion(data_dir=Path("data"), faiss_dir=Path("faiss"))
            data_ingestion.ingest_files(upload_files)
                

if __name__ == "__main__":
    # Example usage
    data_ingestion = SingleDocumentChatDataIngestion(data_dir=Path("data"), faiss_dir=Path("faiss"))
    retriever = FAISS.load_local("faiss_index", data_ingestion.model_loader.load_embeddings())
    
    session_id = "test_session"
    conversational_rag = ConversationalRag(session_id=session_id, retriever=retriever)
    
    # Add more logic to interact with the ConversationalRag instance as needed