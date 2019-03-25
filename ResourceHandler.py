"""
Security course
Chacun Guillaume, Feuillade Julien
HE-Arc, Neuchâtel
2018-2019

***

ResourceHandler.py
"""

import array

class ResourceHandler(object):
    """
    Utility class to handle multiple types of files (wav, images, text). 
    Provides method to read files as bytes and recreate them from those bytes array.
    """

    @staticmethod
    def read_as_bytes(filename):
        """
        Reads file and returns content as a bytes array.
        """
        with open(filename, "rb") as file:
            bytes = array.array("B")
            bytes.fromstring(file.read())
            return bytes
    
    @staticmethod
    def write_bytes_to_file(bytes, filename):
        """
        Creates a new file and writes bytes data as content.
        """
        try:
            with open(filename, mode="bx") as file:
                file.write(bytes)
        except FileExistsError:
            print(filename, ": File already exists !")

if __name__ == "__main__":
    FILENAME_SOURCE =  "./resources/text/hello_world.txt"
                    # "./resources/images/avengers.png" 
                    # "./resources/audio/hello_world.wav"
    FILENAME_DESTINATION = "./resources/text/hello_world_rewritten.txt"
                        # "./resources/images/avengers_rewritten.png" 
                        # "./resources/audio/hello_world_rewritten.wav"

    # read source file
    bytes = ResourceHandler.read_as_bytes(FILENAME_SOURCE)
    
    print(bytes[0])
    
    # create destination file
    ResourceHandler.write_bytes_to_file(bytes, FILENAME_DESTINATION)