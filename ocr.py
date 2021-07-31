try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


def ocr_core(filename):
    """ OCR processing of images. """

    # Using Pillow to open image and pytesseract to read string in the image
    list_of_words = pytesseract.image_to_string(Image.open(filename)).split()

    # converting results dict to list of only words

    # listing key words
    store_names = ['TESCO', 'MORRISONS', 'M & S', 'M & S FOOD', 'LIDL', 'SAINSBURY\'S', 'ASDA']
    total_price_words = ['TOTAL', 'SUBTOTAL', 'SUB-TOTAL', 'BALANCE DUE', 'DEBIT', 'DUE']

    """Function looks for store name and receipt's total price """

    store_name, first_word_after_total, second_word_after_total = "", "", ""

    # capitalise words in the list
    words = list(map(lambda x: x.upper(), list_of_words))

    # remove empty strings
    while "" in list_of_words:
        list_of_words.remove("")

    # find if store name present
    for store in store_names:
        if store in words:
            store_name = store

    # find if total is in words list
    check = any(item in words for item in total_price_words)
    if check:
        for i in reversed(words):
            if i in total_price_words:
                i_index = words.index(i)
                first_word_after_total = any(map(str.isdigit, words[i_index + 1]))
                second_word_after_total = any(map(str.isdigit, words[i_index + 2]))

                if first_word_after_total:
                    first_word_after_total = words[i_index + 1]
                elif second_word_after_total:
                    second_word_after_total = words[i_index + 2]
                else:
                    pass


    return list_of_words, store_name, first_word_after_total, second_word_after_total










