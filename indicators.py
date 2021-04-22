import config
import numpy as np
class indicators():

    def __init__(self,ind):
        #ind determines which indicactor it is
        self.ind = ind

    #actual indiaqctors
    def sma(self):

    #calculations
    def moving_average(self,x, w):
        """
        Closing Prices
        :param x:Sequence of closing prices
        :param w: w is a length for a sequence of ones
        :return: The moving average of the sequence(x) in a list so we can see
        """
        return np.convolve(x, np.ones(w), 'valid') / w