import sys
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from document_portal.exception.custom_exception import DocumentPortalException
from document_portal.logger.cloud_logger import CustomLogger
from document_portal.utils.config_loader import load_config
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
        self.config = load_config()
        log.info("Configuration loaded", config_keys=list(self.config.keys()))
        
    
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
            
    def load_embeddings(self):
        """
        Load the embedding model.
        
        Raises:
            DocumentPortalException: If the embedding model fails to load.
        Returns:
            GoogleGenerativeAIEmbeddings: The loaded embedding model.
        """
        try:
            log.info("Loading embedding model")
            model_name = self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=model_name)
        except Exception as e:
            log.error("Failed to load embedding model", error=str(e))
            raise DocumentPortalException(f"Failed to load embedding model: {e}", sys)
    
    def load_llm(self):
        """ 
        Load the LLM model.

        Raises:
            DocumentPortalException: If the LLM model fails to load.

        Returns:
            GoogleGenerativeAIEmbeddings: The loaded LLM model.
        """
        try:
            llm_block = self.config["llm"]
            log.info("Loading LLM")
            llm_provider = os.getenv("LLM_PROVIDER", "groq") # Default to 'groq' if not set
            if llm_provider not in llm_block:
                log.error("LLM provider not found in configuration", llm_provider=llm_provider)
                raise DocumentPortalException(f"LLM provider '{llm_provider}' not found in configuration", sys)

            llm_config = llm_block[llm_provider]
            provider = llm_config.get("provider")
            model_name = llm_config.get("model_name")
            temperature = llm_config.get("temperature")
            max_tokens = llm_config.get("max_tokens")
            
            log.info("LLM configuration", provider=provider, model_name=model_name, temperature=temperature, max_tokens=max_tokens)

            if provider == "google":
                llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
                return llm
            
            elif provider == "groq":
                llm=ChatGroq(
                    model=model_name,
                    api_key=self.api_keys["GROQ_API_KEY"], #type: ignore
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return llm
            
            else:
                log.error("Unknown LLM provider", provider=provider)
                raise DocumentPortalException(f"Unknown LLM provider: {provider}", sys)
        except Exception as e:
            log.error("Failed to load LLM", error=str(e))
            raise DocumentPortalException(f"Failed to load LLM: {e}", sys)


if __name__ == "__main__":
    loader = ModelLoader()
    
    # Test embedding model loading
    embeddings = loader.load_embedding_model()
    print(f"Embedding Model Loaded: {embeddings}")
    
    # Test the ModelLoader
    result=embeddings.embed_query("Hello, how are you?")
    print(f"Embedding Result: {result}")
    
    # Test LLM loading based on YAML config
    llm = loader.load_llm()
    print(f"LLM Loaded: {llm}")
    
    # Test the ModelLoader
    result=llm.invoke("Hello, how are you?")
    print(f"LLM Result: {result.content}")