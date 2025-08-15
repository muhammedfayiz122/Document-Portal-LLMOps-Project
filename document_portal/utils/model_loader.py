import sys
from document_portal.exception.custom_exception import DocumentPortalException
from document_portal.logger.cloud_logger import CustomLogger
from dotenv import load_dotenv
import os

log = CustomLogger().get_logger(__name__)

class ModelLoader():
    """
    Utility class to load LLM models and embedding models.
    """
    def __init__(self):
        
        
        load_dotenv()
        self._validate_env()
        
    
    def _validate_env(self):
        """
        Validate that necessary environment variables are set.
        Ensure API keys and model names are provided.
        """
        required_vars = ["GOOGLE_API_KEY","GROQ_API_KEY"]
        self.api_keys = {key: os.getenv(key) for key in required_vars}
        missing = [key for key, value in self.api_keys.items() if not key]
        if missing:
            log.error("Missing environment variables", missing_vars=missing)
            raise DocumentPortalException(f"Missing environment variables", sys)
        log.info("Environment variables validated", api_keys=self.api_keys)
            
    def load_embedding_model(self):
        """
        Load the embedding model.
        """
        pass
    
    def load_llm(self):
        pass
    
    