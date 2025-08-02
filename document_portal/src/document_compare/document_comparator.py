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
        load_dotenv()
        self.logger = CustomLogger().get_logger(__file__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()
        self.parser = JsonOutputParser()
        self.fixing_parser = OutputFixingParser()
        self.prompt = PROMPT_REGISTERY["document_comparison"]
        self.chain = self.prompt | self.llm | self.parser | self.fixing_parser
        self.logger.info("DocumentComparatorLLM initialized")

    def compare_documents(self):
        """Compares two documents using LLM"""
        try:
            pass
        except Exception as e:
            self.logger.error(f"Error in document comparison: {e}")
            raise DocumentPortalException("Failed to compare documents") from e

    def _format_response(self):
        """Formats the response from the LLM"""
        try:
            pass
        except Exception as e:
            self.logger.error(f"Error formatting response: {e}")
            raise DocumentPortalException("Failed to format response") from e