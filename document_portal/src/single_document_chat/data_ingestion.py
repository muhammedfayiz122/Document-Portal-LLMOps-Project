import uuid
from pathlib import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from document_portal.logger.cloud_logger import CustomLogger
from document_portal.exception.custom_exception import DocumentPortalException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Faiss

class SingleDocumentChatDataIngestion:
    """
    Handles data ingestion for single document chat
    """
    def __init__(self, base_dir) -> None:
        try:
            self.logger = CustomLogger().get_logger(__file__)
            self.base_dir = Path(base_dir)
            base_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.logger.error(f"Error initializing SingleDocumentChatDataIngestion: {e}")
            raise DocumentPortalException("Failed to initialize data ingestion") from e
    
    def ingest_files(self):
        try: pass
        except Exception as e:
            self.logger.error(f"Error ingesting files: {e}")
            raise DocumentPortalException("Failed to ingest files") from e
        
    def _create_retriever(self, documents):
        try:
            pass
        except Exception as e:
            self.logger.error(f"Error creating retriever: {e}")
            raise DocumentPortalException("Failed to create retriever") from e

