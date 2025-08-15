import sys
from datetime import datetime, timezone
from io import IOBase
from pathlib import Path
from typing import Any
from uuid import uuid4

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from document_portal.exception.custom_exception import DocumentPortalException
from document_portal.logger.cloud_logger import CustomLogger
from document_portal.utils.model_loader import ModelLoader

class DocumentIngestor:
    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt'}
    def __init__(
        self, 
        session_id: str | None = None, 
        temp_dir: str = "data/multi_document_chat", 
        faiss_dir: str = "faiss_index"
        ) -> None:
        """
        Initialize the DocumentIngestor.

        This method:
            1. Sets up directories for temporary files and FAISS index.
            2. Validates the session ID or generates a new one.
            3. Initializes the ModelLoader for loading models.
            
        Args:
            session_id (str | None, optional): The ID of the session. Defaults to None.
            temp_dir (str, optional): The temporary directory for storing files. Defaults to "data/multi_document_chat".
            faiss_dir (str, optional): The directory for storing FAISS index files. Defaults to "faiss_index".

        Raises:
            DocumentPortalException: _description_
        """
        try:
            self.log = CustomLogger().get_logger(__name__)
            
            # base dirs
            self.temp_dir = Path(temp_dir)
            self.faiss_dir = Path(faiss_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)
            
            # Session Managing
            self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
            self.session_temp_dir = self.temp_dir / self.session_id
            self.session_faiss_dir = self.faiss_dir / self.session_id
            self.session_temp_dir.mkdir(parents=True, exist_ok=True)
            self.session_faiss_dir.mkdir(parents=True, exist_ok=True)
            
            self.model_loader = ModelLoader()
            
            self.log.info(
                "DocumentIngestor initialized",
                temp_base=str(self.temp_dir),
                faiss_base=str(self.faiss_dir),
                session_id=self.session_id,
                temp_path=str(self.session_temp_dir),
                faiss_path=str(self.session_faiss_dir),
            )
        except Exception as e:
            self.log.error("Failed to initialize DocumentIngestor", error=str(e))
            raise DocumentPortalException("Initialization error in DocumentIngestor", sys)    

    def ingest_files(self, upload_files: list[IOBase]) -> Any:
        """
        Process and ingest multiple uploaded documents into a FAISS vector store retriever.

        This method:
            1. Validates file extensions against supported formats.
            2. Saves uploaded files into the session's `raw_docs` directory with unique names.
            3. Loads document content using the appropriate loader based on file type.
            4. Splits documents into chunks for embedding.
            5. Creates and stores a FAISS index for retrieval.
        Args:
            uploaded_files (list[IOBase]): List of uploaded file-like objects with `.name` and `.read()`.

        Returns:
            BaseRetriever: FAISS retriever for the ingested documents.

        Raises:
            DocumentPortalException: If no valid documents are loaded or ingestion fails.
        """
        try:
            documents = []
            for file in upload_files:
                # Skip if the file format not in the mentioned formats
                extension = Path(file.name).suffix.lower() #type: ignore
                if extension not in self.SUPPORTED_EXTENSIONS:
                    self.log.warning("Unsupported file skipped", file_name=file.name, extension=extension) #type: ignore
                    continue
                
                # Create a unique filename for the session
                session_filename = f"{uuid4().hex[:8]}{extension}"
                session_file_path = self.session_temp_dir / session_filename
                
                # Save the file to the session's directory
                with open(session_file_path, "wb") as f:
                    f.write(file.read())
                self.log.info("File saved for ingestion", file_name=session_filename, saved_as=str(session_file_path))    
                    
                # Select the loader based on its type
                if extension == '.pdf':
                    loader = PyPDFLoader(str(session_file_path))
                elif extension == '.docx':
                    loader = Docx2txtLoader(str(session_file_path))
                elif extension == '.txt':
                    loader = TextLoader(str(session_file_path), encoding="utf-8")
                else:
                    self.log.warning("Unsupported file type for loading", file_name=file.name, extension=extension) #type: ignore
                    continue
                
                # Load the document content
                doc = loader.load()
                documents.extend(doc)

            if not documents:
                self.log.error("No valid documents found")
                raise DocumentPortalException("No valid documents found", sys)
            self.log.info("Documents loaded successfully", total_docs=len(documents), session_id=self.session_id)
            

            # Create FAISS index
            self._create_retriever(documents)
        except Exception as e:
            self.log.error("Failed to initialize DocumentIngestor", error=str(e))
            raise DocumentPortalException("Intialization error in DocumentIngestor", sys)
            
        
    def _create_retriever(self, documents: list) -> Any:
        """
        Create a retriever for the ingested documents.
        
        This method:
            1. Splits the documents into chunks.
            2. Loads the embedding model.
            3. Creates a FAISS vector store from the chunks.
            4. Saves the vector store to the session's FAISS directory.
            
        Args:
            documents (list): List of loaded documents to be processed.
            
        Returns:
            BaseRetriever: FAISS retriever for the ingested documents.
        
        Raises:
            DocumentPortalException: If the retriever creation fails.
        """
        try:
            # Split the documents into chunks
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=300,
            )
            chunks = splitter.split_documents(documents)
            self.log.info("Documents split into chunks", total_chunks=len(chunks), session_id=self.session_id)
            
            # Load the embedding model
            embeddings = self.model_loader.load_embeddings()

            # Create a FAISS vector store from the chunks
            vector_store = FAISS.from_documents(documents=chunks, embedding=embeddings)
            
            # Save the vector store to the session's FAISS directory
            vector_store.save_local(str(self.session_faiss_dir))
            self.log.info("FAISS index created and saved", faiss_path=str(self.session_faiss_dir), session_id=self.session_id)
            
            # Create a retriever from the vector store
            retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            self.log.info("FAISS retriever created and ready to use", session_id=self.session_id)
            return retriever
        
        except Exception as e:
            self.log.error("Failed to create retriever", error=str(e))
            raise DocumentPortalException("Retrieval error in DocumentIngestor", sys)
            
