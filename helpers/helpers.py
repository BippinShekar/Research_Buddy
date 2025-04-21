import fitz 
import io
from PIL import Image

def pdf_reader(pdf_path: str) -> dict:
    """
    Read a PDF file and extract text content and images.
    
    Args:
        pdf_path (str): Path or URL to the PDF file
        
    Returns:
        dict: Dictionary containing:
            - 'text': Extracted text content from the PDF
            - 'images': List of extracted images as PIL Image objects
    """
    try:
        doc = fitz.open(pdf_path)
        
        text_content = ""
        for page in doc:
            text_content += page.get_text()
            
        images = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Convert to PIL Image
                image = Image.open(io.BytesIO(image_bytes))
                images.append(image)
                
        doc.close()
        
        return {
            "text": text_content,
            "images": images
        }
        
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return {
            "text": "",
            "images": []
        }
