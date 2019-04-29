"""
Security course
Chacun Guillaume, Feuillade Julien
HE-Arc, Neuchâtel
2018-2019

***

ResourceHandler.py
"""

import array
import os

class ResourceHandler(object):
    """
    Utility class to handle multiple types of files (wav, images, text). 
    Provides method to read files as bytes and recreate them from those bytes array.
    """

    @staticmethod
    def get_destinations_filenames(filename_source):
        """
        Returns a tuple of strings. 
        First element is the filename for the encrypted file.
        Second element is the filename for the decrypted file.
        """
        filename_cipher_suffix = "_cipher"
        filename_cipher = ".".join(filename_source.split(".")[:-1]) + \
                            filename_cipher_suffix + \
                            "." + \
                            filename_source.split(".")[-1]

        filename_decipher_suffix = "_decipher"
        filename_decipher = ".".join(filename_source.split(".")[:-1]) + \
                            filename_decipher_suffix + \
                            "." + \
                            filename_source.split(".")[-1]
        return (filename_cipher, filename_decipher)

    @staticmethod
    def read_as_bytes(filename):
        """
        Reads file and returns content as a bytes array.
        """
        try:
            with open(filename, "rb") as file:
                bytes = array.array("B")
                bytes.frombytes(file.read())
                return bytes
        except FileNotFoundError:
            print(f"File not found: {filename}")
            exit()

    @staticmethod
    def write_bytes_to_file(bytes, filename):
        """
        Creates a new file and writes bytes data as content.
        """
        try:
            with open(filename, mode="bx") as file:
                file.write(bytes)
        except FileExistsError:
            os.remove(filename)
            ResourceHandler.write_bytes_to_file(bytes, filename)
        except Exception as e:
            print(e)