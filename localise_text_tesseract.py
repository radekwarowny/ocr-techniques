from pytesseract import Output
from PIL import Image
import pytesseract
import argparse
import cv2

filename = 'tesco/asda.png'


def ocr_box_bounding(filename):
    # # construct the argument parser and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd")
    # ap.add_argument("-c", "--min-conf", type=int, default=0, help="minimum confidence value to filter weak text detection")
    # args = vars(ap.parse_args())
    #
    # # load the input image, convert it from BGR to RGB channel ordering,
    # # and use Tesseract to localise each area of text in the input image
    # image = cv2.imread(args["image"])
    #
    # text = pytesseract.image_to_string(Image.open(filename))

    # load the input image, convert it from BGR to RGB channel ordering,
    # and use Tesseract to localise each area of text in the input image
    image = cv2.imread(filename)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

    # loop over each of the individual text localisations
    for i in range(0, len(results["text"])):
        # extract the bounding box coordinates of the text region from
        # the current result
        x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]

        # extract the OCR text itself along with the confidence of the text localisation
        text = results["text"][i]
        conf = int(results["conf"][i])

        # filter out weak confidence text localisations
        if conf > 50:
            # display the confidence and text to out terminal
            # print("Confidence: {}".format(conf))
            # print("Text: {}".format(text))
            # print("")

            # strip out non-ASCII text so we can draw the text on the image
            # using OpenCV, then draw a bounding box around the text along with the text itself
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(image, text, (x, y -10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    # show the output image

    #cv2.imshow("Image", image)
    #cv2.waitKey(0)

    # converting results dict to list of only words
    list_of_words = results.get('text')
    # listing key words
    store_names = ['TESCO', 'MORRISONS', 'M & S', 'M & S FOOD', 'LIDL', 'SAINSBURY\'S', 'ASDA']
    total_price_words = ['TOTAL', 'SUBTOTAL', 'SUB-TOTAL']

    """Function looks for store name and receipt's total price """

    store_name, first_word_after_total, second_word_after_total = "", "", ""

    # capitalise words in the list
    words = list(map(lambda x: x.upper(), list_of_words))

    # remove empty strings
    while "" in list_of_words:
        list_of_words.remove("")

    # find if store name present
    for store in store_names:
        if store in list_of_words:
            store_name = store
            print('I think this is ', store)

    # find if total is in words list
    check = any(item in words for item in total_price_words)
    if check:
        for i in reversed(words):
            if i in total_price_words:
                i_index = words.index(i)
                word1_after_total = any(map(str.isdigit, words[i_index+1]))
                word2_after_total = any(map(str.isdigit, words[i_index+2]))

                if word1_after_total:
                    print('This is the total', words[i_index+1])
                elif word2_after_total:
                    print('This is the total', words[i_index+2])
                else:
                    print('Not sure what total is.')

    return store_name, first_word_after_total, second_word_after_total

ocr_box_bounding(filename)

