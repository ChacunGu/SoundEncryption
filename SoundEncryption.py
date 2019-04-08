"""
Security course
Chacun Guillaume, Feuillade Julien
HE-Arc, Neuchâtel
2018-2019

***

SoundEncryption.py
"""

import rc4
from ResourceHandler import ResourceHandler

import array
import wave
import audioop

def encrypt_data(key, data, algorithm="rc4"):
    """
    Encrypts data with key and specified algorithm.
    """
    if algorithm == "rc4":
        return rc4.encrypt(key, data)
    #elif algorithm == "rc5":

def decrypt_data(key, data, algorithm="rc4"):
    """
    Decrypts data with key and specified algorithm.
    """
    if algorithm == "rc4":
        return rc4.decrypt(key, data)
    #elif algorithm == "rc5":

def encrypt_decrypt_and_compare(filename, key, is_creating_wav_demo_file=False):
    """
    Opens file, encrypts it, saves its content, decrypts it and compares source file with final file.
    Uses Python's wave library if file is wav and the encrypted version should be listenable (used for preserving
    wav header). This modules only supports wav format PCM (WAVE_FORMAT_PCM: 0x0001).
    """
    filename_cipher, filename_decipher = ResourceHandler.get_destinations_filenames(filename)

    if is_creating_wav_demo_file:
        # Credit: https://stackoverflow.com/a/35530516
        try:
            # load data
            with wave.open(filename) as fd:
                params = fd.getparams()
                frames = fd.readframes(1000000) # 1 million frames max
            data = audioop.reverse(frames, params.sampwidth)

            # encrypt
            encrypted_data = encrypt_data(key, data, "rc4")

            # write encrypted file
            with wave.open(filename_cipher, "wb") as fd:
                fd.setparams(params)
                fd.writeframes(bytes(encrypted_data))

            # decrypt
            decrypted_data = decrypt_data(key, encrypted_data, "rc4")

            # write decrypted file
            with wave.open(filename_decipher, "wb") as fd:
                fd.setparams(params)
                fd.writeframes(bytes(decrypted_data))
                
            # compare source and destination files
            compare_source_and_result(array.array("B", data), decrypted_data)

        except wave.Error:
            # Wave module limitations: https://stackoverflow.com/a/27101840
            print(f"{filename} is not of a supported wav type. Python's wave library only supports: PCM (WAVE_FORMAT_PCM: 0x0001)")
    else:
        # load data
        data = ResourceHandler.read_as_bytes(filename)
        
        # encrypt
        encrypted_data = encrypt_data(key, data, "rc4")

        # write encrypted file
        ResourceHandler.write_bytes_to_file(array.array("B", encrypted_data), filename_cipher)

        # decrypt
        decrypted_data = decrypt_data(key, encrypted_data, "rc4")

        # write decrypted file
        ResourceHandler.write_bytes_to_file(array.array("B", decrypted_data), filename_decipher)

        # compare source and destination files
        compare_source_and_result(data, decrypted_data)

def compare_source_and_result(source, result):
    """
    Compares source and result files and prints result.
    """
    if source.tolist() == result:
        print("Equal")
    else:
        print("Different") 


if __name__ == "__main__":
    FILES = ["./resources/audio/M1F1-Alaw-AFsp.wav",    # 0
             "./resources/audio/bf1.wav",               # 1
             "./resources/audio/organfinale.wav",       # 2
             "./resources/audio/addf8-Alaw-GW.wav",     # 3

             "./resources/images/avengers.png",         # 4
             "./resources/text/hello_world.txt"         # 5
            ]

    KEY = "Wddddddiki"
    FILENAME_SOURCE = FILES[0]
    CREATE_WAV_DEMO_FILE = False

    encrypt_decrypt_and_compare(FILENAME_SOURCE, KEY, is_creating_wav_demo_file=CREATE_WAV_DEMO_FILE)
        