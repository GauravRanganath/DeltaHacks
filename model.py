
import cv2
import sys
import numpy as np
import keras
import random
import time
import pickle


from keras.models import load_model


class ASL_model(object):
    def __init__(self):
        self.model = load_model('model_edged.h5')
        self.alphabet = self.generate_alphabet_dict()
        self.camera = cv2.VideoCapture(0)

        self.setup()

        # VARIABLES INITIALIZATION
        self.IMG_SIZE = 100
        self.letter = ''  # temporary letter
        self.LETTERS = np.array([], dtype='object')  # array of pred. letters

        self.START = False  # start/pause controller

        # supportive text
        self.description_text_1 = "Press 'S' to Start/Pause gesture recognition."
        self.description_text_2 = "Press F to finish and to see how you did!"
        self.description_text_3 = "Press 'Q' to quit."

    def setup(self):
        def nothing(x):
            pass

        # set the ration of main video screen

        # set track bar of threshold values for Canny edge detection
        # more on Canny edge detection here:
        # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html

    def generate_alphabet_dict(self):
        alphabet = {chr(i+96).upper(): i for i in range(1, 27)}
        alphabet['del'] = 27
        alphabet['nothing'] = 28
        alphabet['space'] = 29
        return alphabet

    def predict(self, frame, letter_to_get):
        correct_letter = False

        # black image for the output

        # set the corners for the square to initialize the model picture frame
        x_0 = int(frame.shape[1] * 0.1)
        y_0 = int(frame.shape[0] * 0.25)
        x_1 = int(x_0 + 250)
        y_1 = int(y_0 + 250)

        # MODEL IMAGE INITIALIZATION
        hand = frame.copy()[y_0:y_1, x_0:x_1]  # crop model image
        # convert to grayscale
        gray = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY)
        # noise reduction
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        blurred = cv2.erode(blurred, None, iterations=2)
        blurred = cv2.dilate(blurred, None, iterations=2)
        # get the values from tack bar

        edged = cv2.Canny(blurred, 50, 100)  # apply edge detector

        model_image = ~edged  # invert colors
        model_image = cv2.resize(
            model_image,
            dsize=(self.IMG_SIZE, self.IMG_SIZE),
            interpolation=cv2.INTER_CUBIC
        )
        model_image = np.array(model_image)
        model_image = model_image.astype('float32') / 255.0

        try:
            model_image = model_image.reshape(
                1, self.IMG_SIZE, self.IMG_SIZE, 1)
            predict = self.model.predict(model_image)
            for values in predict:

                if np.all(values < 0.5):
                    # if probability of each class is less than .5 return a message
                    return 'Cannot classify :('
                else:
                    predict = np.argmax(predict, axis=1) + 1
                    letter = self.get_class_label(predict, self.alphabet)

                    if letter == letter_to_get:
                        return "YAY"
                        correct_letter = True
                        letter_to_get = self.next_letter(letter_to_get)

                        # if not text_updated:
                        #     text_updated = True
                        #     game_text = random.choice(
                        #         ["Nice one!", "You're a pro!", "You're a natural!", "Have you been practicing?", "You're on a roll!"])
                    else:
                        return None

        except:
            pass

            # if not self.START:
            #     paused_text = 'Paused'
            # else:
            #     paused_text = ''

            # TEXT INITIALIZATION
            # paused text
            # cv2.putText(
            #     img=frame,
            #     text=paused_text,
            #     org=(x_0+140, y_0+195),
            #     fontFace=cv2.FONT_HERSHEY_PLAIN,
            #     color=(0, 0, 255),
            #     fontScale=1
            # )

            # # helper texts
            # cv2.putText(
            #     img=frame,
            #     text=self.description_text_1,
            #     org=(10, 440),
            #     fontFace=cv2.FONT_HERSHEY_PLAIN,
            #     color=(255, 255, 255),
            #     fontScale=1
            # )

            # cv2.putText(
            #     img=frame,
            #     text=self.description_text_2,
            #     org=(10, 455),
            #     fontFace=cv2.FONT_HERSHEY_PLAIN,
            #     color=(255, 255, 255),
            #     fontScale=1
            # )

            # cv2.putText(
            #     img=frame,
            #     text='Place your hand here:',
            #     org=(x_0-30, y_0-10),
            #     fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
            #     color=(255, 255, 255),
            #     fontScale=1
            # )

            # # current letter
            # cv2.putText(
            #     img=frame,
            #     text=letter,
            #     org=(x_0+10, y_0+20),
            #     fontFace=cv2.FONT_HERSHEY_PLAIN,
            #     color=(255, 255, 255),
            #     fontScale=1
            # )

            # cv2.putText(
            #     img=frame,
            #     text=game_text,
            #     org=(288, 225),
            #     fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
            #     color=(255, 255, 255),
            #     fontScale=1
            # )

            # draw rectangle for hand placement
            # cv2.rectangle(frame, (x_0, y_0), (x_1, y_1), (0, 255, 0), 2)

            # display the resulting frames

            # if cv2.waitKey(30) & 0xFF == ord('s'):
            #     self.START = not self.START

            # if cv2.waitKey(30) & 0xFF == ord('f'):
            #     break

    def get_class_label(self, val, dictionary):
        """
        Function returns the key (Letter: a/b/c/...) value from the alphabet dictionary
        based on its class index (1/2/3/...)
        """
        for key, value in dictionary.items():
            if value == val:
                return key

    def next_letter(self, cur_letter):
        cur_letter_ord = ord(cur_letter)
        return chr(cur_letter_ord + 1)

    def quit(self):
        self.camera.release()
        cv2.destroyAllWindows()
