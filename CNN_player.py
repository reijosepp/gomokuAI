import numpy as np
from keras.models import load_model
import tensorflow.compat.v2 as tf


class CNNPlayer:

    def __init__(self, model_file):
        self.model = load_model(model_file)

    def move(self, board, color):
        b = np.array([board]) * color
        pred = self.model.predict(b,verbose = 0)
        pred = ((1 - np.abs(board)) * pred.reshape(1, 15, 15)).reshape(225)

        return np.unravel_index(np.random.choice(np.arange(0, 225), p = pred / np.sum(pred)), shape=(15, 15))
