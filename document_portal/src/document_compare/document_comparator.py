import sys
from dotenv import load_dotenv
import pandas as pd
from document_portal.logger.cloud_logger import CustomLogger
from document_portal.exception.custom_exception import DocumentPortalException
from document_portal.model.models import *
# from document_portal.prompts.prompt_library import PROMPT_REGISTRY
from langchain_core.output_parsers import JsonOutputParser

class DocumentComparatorLLM:
    """
    Handles LLM operations for document comparison
    """
    def __init__(self) -> None:
        pass
    
    def compare_documents(self):
        pass

    def _format_response(self):
        pass