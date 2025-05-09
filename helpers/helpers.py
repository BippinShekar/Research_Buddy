import fitz
import io
import re
from PIL import Image
from typing import List, Dict
from enums.environmet_variables import EnvironmentVariables

class PDFProcessor:
    """
    A class for processing PDF files, including extracting text, images, and hyperlinks.
    """

    def __init__(self, pdf_path: str):
        """
        Initialize the PDFProcessor with the path to a PDF file.

        Args:
            pdf_path (str): The file path to the PDF to be processed.
        """
        self.pdf_path = pdf_path

    def extract_text(self) -> str:
        """
        Extract all text content from the PDF.

        Returns:
            str: The concatenated text extracted from all PDF pages.
        """
        try:
            doc = fitz.open(self.pdf_path)
            text_content = ""
            for page in doc:
                text_content += page.get_text()
            doc.close()
            return text_content
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return ""

    def extract_images(self) -> List[Image.Image]:
        """
        Extract all images from the PDF.

        Returns:
            list: A list of PIL Image objects extracted from the PDF.
        """
        images = []
        try:
            doc = fitz.open(self.pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                image_list = page.get_images()
                for img in image_list:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    images.append(image)
            doc.close()
        except Exception as e:
            print(f"Error extracting images: {str(e)}")
        return images

    def extract_text_and_images(self) -> Dict[str, object]:
        """
        Extract both text and images from the PDF.

        Returns:
            dict: A dictionary containing:
                - 'text': The extracted text from the PDF.
                - 'images': A list of extracted images as PIL Image objects.
        """
        return {
            "text": self.extract_text(),
            "images": self.extract_images()
        }

    def extract_hyperlinks(self) -> List[str]:
        """
        Extract HTTPS hyperlinks from the text content of the PDF using a regex pattern from environment variables.

        Returns:
            list: A list of HTTPS URLs found in the PDF text.
        """
        try:
            text = self.extract_text()
            pattern = EnvironmentVariables.REFERENCE_PATTER.value_from_env
            return re.findall(pattern, text)
        except Exception as e:
            print(f"Error extracting hyperlinks: {str(e)}")
            return []