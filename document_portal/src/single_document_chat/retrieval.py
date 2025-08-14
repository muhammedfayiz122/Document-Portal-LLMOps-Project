import sys 
import os
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from document_portal.utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from document_portal.prompts.prompt_library import PROMPT_REGISTRY
from model.models import PromptType

class ConversationalRag:
    def __init__(self, session_id, retriever):
        try:
            self.logger = CustomLogger().get_logger(__file__)
            self.session_id = session_id
            self.retriever = retriever
            self.llm = self._load_llm()
            self.contextualize_prompt = PROMPT_REGISTRY.get(PromptType.CONTEXTUALIZE_QUESTION.value)
            self.qa_prompt = PROMPT_REGISTRY.get(PromptType.CONTEXTUALIZE_QA.value)
            self.history = ChatMessageHistory(session_id=session_id)
        except Exception as e:
            self.logger.error(f"Error initializing ConversationalRag: {e}")
            raise DocumentPortalException("Failed to initialize ConversationalRag") from e
    
    def _load_llm(self):
        try:
            model_loader = ModelLoader()
            llm = model_loader.load_llm()
            self.logger.info("LLM loaded successfully")
            return llm
        except Exception as e:
            self.logger.error(f"Error loading LLM: {e}")
            raise DocumentPortalException("Failed to load LLM") from e
