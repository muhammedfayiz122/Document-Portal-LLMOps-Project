import uuid
from pathlib import Path
import sys
from datetme import datetime, timezone
from langchain_community.document_loaders import PyPDFLoader
from document_portal.logger.cloud_logger import CustomLogger
from document_portal.exception.custom_exception import DocumentPortalException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Faiss

class SingleDocumentChatDataIngestion:
    """
    Handles data ingestion for single document chat
    """
    def __init__(self, data_dir, faiss_dir) -> None:
        try:
            self.logger = CustomLogger().get_logger(__file__)
            
            self.data_dir = Path(data_dir)
            data_dir.mkdir(parents=True, exist_ok=True)

            self.faiss_dir = Path(faiss_dir)
            faiss_dir.mkdir(parents=True, exist_ok=True)
            
            self.model_loader = ModelLoader()
            
            self.logger.info("SingleDocumentChatDataIngestion initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing SingleDocumentChatDataIngestion: {e}")
            raise DocumentPortalException("Failed to initialize data ingestion") from e
    
    def ingest_files(self, upload_files):
        try:
            documents = []
            
            for upload_file in upload_files:
                unique_filename = f"{uuid.uuid4()}_{upload_file.name}"
                with open(self.data_dir / unique_filename, 'wb') as f:
                    f.write(upload_file.read())
                loader = PyPDFLoader(self.data_dir / unique_filename)
                documents.extend(loader.load())

        except Exception as e:
            self.logger.error(f"Error ingesting files: {e}")
            raise DocumentPortalException("Failed to ingest files") from e
        
    def _create_retriever(self, documents):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            split_docs = splitter.split_documents(documents)
            self.logger.info(f"Split documents into {len(split_docs)} chunks")
            
            embeddings = self.model_loader.load_embeddings()
            vector_store = Faiss.from_documents(split_docs, embeddings)
            
            # Save the vector store to disk
            vector_store.save_local(self.faiss_dir / "faiss_index")
            
            retriever = vector_store.as_retriever(search_kwargs={"k": 5})
            self.logger.info("Retriever created successfully")
        except Exception as e:
            self.logger.error(f"Error creating retriever: {e}")
            raise DocumentPortalException("Failed to create retriever") from e

