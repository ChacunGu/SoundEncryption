"""
Security course
Chacun Guillaume, Feuillade Julien
HE-Arc, Neuchâtel
2018-2019

***

RandomNumberGenerator.py
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

import rc4

class RandomNumberGenerator:

    def __init__(self, key):
        self.key = key = [ord(c) for c in key]
        self.generator = rc4.KeyStream(self.key)

    def generate(self):
        """
        Generates and returns a new random number.
        """
        return next(self.generator)

    def display_random_image(self, width=1000):
        """
        Displays a random image.
        """
        img = [[self.generate() for j in range(width)] for i in range(width)]
        plt.imshow(img)
        plt.show()

    def verify_randomness(self, nb_tests=50, nb_samples=1000, signal_amplitude=255, sin_freq=50):
        """
        Computes and displays Pearson Correlations on a raw random signal and the same signal added to a
        sinus.

        <<< 
        Correlations are never lower than -1. A correlation of -1 indicates that the data points in a scatter plot lie exactly on a straight descending line; the two variables are perfectly negatively linearly related.
        A correlation of 0 means that two variables don't have any linear relation whatsoever. However, some non linear relation may exist between the two variables.
        Correlation coefficients are never higher than 1. A correlation coefficient of 1 means that two variables are perfectly positively linearly related; the dots in a scatter plot lie exactly on a straight ascending line.
        >>>
        Source: https://www.spss-tutorials.com/pearson-correlation-coefficient/
        """
        raw_random = np.mean([pd.Series([self.generate() for i in range(nb_samples)]).autocorr() for i in range(nb_tests)])
        random_with_sinus = np.mean([pd.Series([self.generate() + math.sin(i/sin_freq) * signal_amplitude
                                                for i in range(nb_samples)]).autocorr() for _ in range(nb_tests)])
        print("Autocorrelation for random signal: %0.5f" % raw_random)
        print("Autocorrelation for sinus added to random signal: %0.5f" % random_with_sinus)

    def plot_random_and_semi_random(self, nb_samples=1000, signal_amplitude=255, sin_freq=50):
        """
        Computes and plots a random signal and the same signal added to a sinus.
        """
        x = np.linspace(0, nb_samples, nb_samples+1)

        # compute signals
        raw_random = pd.Series([self.generate() for i in range(nb_samples)])
        sinus = pd.Series([math.sin(i/sin_freq) * signal_amplitude for i in range(nb_samples)])
        random_with_sinus = pd.Series([rdm + sin for rdm, sin in zip(raw_random, sinus)])
        
        # plot signals
        plt.subplot(2, 1, 1)
        RandomNumberGenerator.plotSignal(x, raw_random[x], "Random signal", show=False)
        plt.subplot(2, 1, 2)
        RandomNumberGenerator.plotSignal(x, sinus[x], color="b", show=False)
        RandomNumberGenerator.plotSignal(x, random_with_sinus[x], "Random signal with sinus", show=True)

    @staticmethod
    def plotSignal(x, y, title="", x_label="x", y_label="y", color="r", show=True):
        """
        Plots given signal with matplotlib.
        """
        plt.plot(x, y, color)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        if show:
            plt.show()