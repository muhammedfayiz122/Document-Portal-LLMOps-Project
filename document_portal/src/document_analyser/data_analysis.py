from document_portal.exception.custom_exception import DocumentPortalException
from document_portal.logger.cloud_logger import CustomLogger
class DocumentHandler:
    """
    Handles PDF read/write operations
    """
    def __init__(self) -> None:
        try:
            self.logger = CustomLogger().get_logger(__file__)
            