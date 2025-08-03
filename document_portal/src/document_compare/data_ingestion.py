import sys
from pathlib import Path
import fitz
from document_portal.logger.cloud_logger import CustomLogger
from document_portal.exception.custom_exception import DocumentPortalException

class DocumentComparator:
    """
    Handles PDF comparison operations
    """
    def __init__(self, base_dir) -> None:
        self.logger = CustomLogger().get_logger(__file__)
        self.base_dir = Path(base_dir)
        base_dir.mkdir(parents=True, exist_ok=True)
    
    def delete_existing_files(self):
        try:
            pass
        except Exception as e:
            self.logger.error(f"Error deleting existing files: {e}")
            raise DocumentPortalException("Failed to delete existing files") from e

    def save_upload_files(self, reference_file: Path, actual_file: Path):
        try:
            self.delete_existing_files()
            self.logger.info("Existing files deleted successfully")

            ref_path = self.base_dir / reference_file.name
            act_path = self.base_dir / actual_file.name

            if not reference_file.name.endswith('.pdf') or not actual_file.name.endswith('.pdf'):
                raise ValueError("Reference and actual files must be PDFs.")

            with open(ref_path, 'wb') as ref_f, open(act_path, 'wb') as act_f:
                ref_f.write(reference_file.getbuffer())
                act_f.write(actual_file.getbuffer())

            self.logger.info("Uploaded files saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving uploaded files: {e}")
            raise DocumentPortalException("Failed to save uploaded files") from e
        
    def read_pdf(self, pdf_path):
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF file {pdf_path} is encrypted and cannot be read.")
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.strip():
                        all_text.append(f"Page {page_num + 1}:\n{text}\n")
                self.logger.info(f"Successfully read PDF: {pdf_path}")
                return "\n".join(all_text)
        except Exception as e:  
            self.logger.error(f"Error reading PDF: {e}")
            raise DocumentPortalException("Failed to read PDF") from e