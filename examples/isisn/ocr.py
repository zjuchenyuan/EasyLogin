try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

# you should change this line on Windows
# on ubuntu, just delete this line...
pytesseract.pytesseract.tesseract_cmd = r'D:\Software\Tesseract-OCR\tesseract.exe'

def ocr(image):
    return pytesseract.image_to_string(image)