from pathlib import Path
from document_portal.exception.custom_exception import DocumentPortalException
from document_portal.logger.cloud_logger import CustomLogger
from document_portal.utils.model_loader import ModelLoader
from uuid import uuid4
import sys
import os

class DocumentIngestor:
    def __init__(self, temp_dir, faiss_dir):
        self.log = CustomLogger().get_logger(__name__)
        self.temp_dir = temp_dir
        os.makedirs(self.temp_dir, exist_ok=True)
        self.faiss_dir = faiss_dir
        os.makedirs(self.faiss_dir, exist_ok=True)
        
        # Session Managing
        self.session_folder = f"session_{uuid4().hex}"
        
        model = 
        
        

    def ingest_files(self, upload_files: Path) -> None:
        """
        Save the uploaded file in session and load it.

        Args:
            upload_files (Path): The path to the uploaded files.

        Returns:
            _type_: _description_
        """
        try:
            pass
        except Exception as e:
            self.log.error("Failed to initialize DocumentIngestor", error=str(e))
            raise DocumentPortalException("Intialization error in DocumentIngestor", sys)
            
        
    def _create_retriever(self):
        """
        Create a retriever for the ingested documents.
        """
        try:
            pass
        except Exception as e:
            self.log.error("Failed to create retriever", error=str(e))
            raise DocumentPortalException("Retrieval error in DocumentIngestor", sys)
            
