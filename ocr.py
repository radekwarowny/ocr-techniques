try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


def ocr_core(filename):
    """ OCR processing of images. """

    # Using Pillow to open image and pytesseract to read string in the image
    text = pytesseract.image_to_string(Image.open(filename))
    # print(filename)

    return text

# print(ocr_core('noisy.png'))

# print(ocr_core('asda.png'))

# print(ocr_core('Tesco.jpg'))



