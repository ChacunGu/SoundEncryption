"""
Security course
Chacun Guillaume, Feuillade Julien
HE-Arc, Neuchâtel
2018-2019

***

RandomNumberGenerator.py
"""

import matplotlib.pyplot as plt

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