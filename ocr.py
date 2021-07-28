try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


def ocr_core(filename):
    """ OCR processing of images. """
    pytesseract.pytesseract.tesseract_cmd = '/app/vendor/tesseract-ocr/bin/tesseract'
    # Using Pillow to open image and pytesseract to read string in the image
    text = pytesseract.image_to_string(Image.open(filename))
    # print(filename)

    return text

# print(ocr_core(noisy.png))

