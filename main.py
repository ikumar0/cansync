import easygui
import pytesseract

filename = easygui.fileopenbox()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
print(pytesseract.image_to_string(filename))

