"""
Security course
Chacun Guillaume, Feuillade Julien
HE-Arc, Neuchâtel
2018-2019

***

SoundEncryption.py
"""

import rc4
from rc5 import RC5
from ResourceHandler import ResourceHandler
from RandomNumberGenerator import RandomNumberGenerator

import array
import audioop
import datetime
import sys
import wave

def encrypt_data(key, data, algorithm="rc4"):
    """
    Encrypts data with key and specified algorithm.
    """
    if algorithm == "rc4":
        return rc4.encrypt(key, data)
    elif algorithm == "rc5":
        cryptor = RC5(key)
        cryptor.mode = "CBC"
        return cryptor.encrypt(bytes(data))

def decrypt_data(key, data, algorithm="rc4"):
    """
    Decrypts data with key and specified algorithm.
    """
    if algorithm == "rc4":
        return rc4.decrypt(key, data)
    elif algorithm == "rc5":
        cryptor = RC5(key)
        cryptor.mode = "CBC"
        return cryptor.decrypt(bytes(data))

def encrypt_decrypt_and_compare(filename, key, algorithm="rc4", is_creating_wav_demo_file=False):
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
                data = fd.readframes(1000000) # 1 million frames max

            # encrypt
            encrypted_data = encrypt_data(key, data, algorithm)

            # write encrypted file
            with wave.open(filename_cipher, "wb") as fd:
                fd.setparams(params)
                fd.writeframes(bytes(encrypted_data))

            # decrypt
            decrypted_data = decrypt_data(key, encrypted_data, algorithm)

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
        encrypted_data = encrypt_data(key, data, algorithm)

        # write encrypted file
        ResourceHandler.write_bytes_to_file(array.array("B", encrypted_data), filename_cipher)

        # decrypt
        decrypted_data = decrypt_data(key, encrypted_data, algorithm)

        # write decrypted file
        ResourceHandler.write_bytes_to_file(decrypted_data, filename_decipher)

        # compare source and destination files
        compare_source_and_result(data, decrypted_data)

def compare_source_and_result(source, result):
    """
    Compares source and result files and prints result.
    """
    print(source[-10:], len(source))
    print(result[-10:], len(result))
    if source == result:
        print("Source and destination files are equal !")
    else:
        print("Source and destination files are different :(") 

def standalone_encrypt(filename, key, algorithm="rc4"):
    """
    Opens file, encrypts it and saves its content.
    """
    filename_cipher = ResourceHandler.get_destinations_filenames(filename)[0]

    # load data
    data = ResourceHandler.read_as_bytes(filename)
    
    # encrypt
    encrypted_data = encrypt_data(key, data, algorithm)

    # write encrypted file
    ResourceHandler.write_bytes_to_file(array.array("B", encrypted_data), filename_cipher)

def standalone_decrypt(filename, key, algorithm="rc4"):
    """
    Opens file, decrypts it and saves its content.
    """
    filename_decipher = ResourceHandler.get_destinations_filenames(filename)[1]

    # load data
    data = ResourceHandler.read_as_bytes(filename)

    # decrypt
    decrypted_data = decrypt_data(key, data, algorithm)

    # write decrypted file
    ResourceHandler.write_bytes_to_file(decrypted_data, filename_decipher)

if __name__ == "__main__":
    help_message = "Help - Available methods: " + \
                   "\n  - Cipher or decipher specified file using specified algorithm & key." + \
                   "\n    Syntax: python SoundEncryption.py [method_id: 1] [mode: cipher, decipher] filename [algorithm: rc4, rc5] key" + \
                   "\n    Example: python SoundEncryption.py 1 cipher file.txt rc4 1234" + \
                   "\n  - Generate a pseudo-random number with RC4 algorithm set with given key. Displays proof of randomness if parameter 'test_randomness' is set to True." + \
                   "\n    Syntax: python SoundEncryption.py [method_id: 2] key [optional: test_randomness: True, False]" + \
                   "\n    Example: python SoundEncryption.py 2 1234 True" + \
                   "\n  - Cipher then deciphers and compare data to verify operations were successful. If processing a .WAV file parameter 'WAV_file_demo' allows to create a listenable version of the ciphered file." + \
                   "\n    Syntax: python SoundEncryption.py [method_id: 3] filename [algorithm: rc4, rc5] key [optional: WAV_file_demo: True, False]" + \
                   "\n    Example: python SoundEncryption.py 3 file.txt 1234 True"

    sys.argv.pop(0)
    nb_args = len(sys.argv)
    if nb_args <= 0:
        print(help_message)
        exit()
    elif nb_args < 2:
        print("Insufficient arguments. \n" + help_message)
        exit()
    elif nb_args > 5:
        print("Too many arguments. \n" + help_message)
        exit()

    # Methods:
    # 5:     [method_id: 1] [mode: cipher, decipher] filename [algorithm: rc4, rc5] key
    # 2-3:   [method_id: 2] key [optional: test_randomness: True, False]
    # 4-5:   [method_id: 3] filename [algorithm: rc4, rc5] key [optional: WAV_file_demo: True, False]

    if nb_args > 1:
        method_id = sys.argv.pop(0)

        if method_id == "1": # cipher or decipher
            try:
                mode = sys.argv[0] if sys.argv[0] == "cipher" or sys.argv[0] == "decipher" else None
                filename = sys.argv[1]
                algorithm = sys.argv[2] if sys.argv[2] == "rc4" or sys.argv[2] == "rc5" else None
                key = sys.argv[3]

                if mode is not None and algorithm is not None:
                    if mode == "cipher":
                        standalone_encrypt(
                            filename, 
                            key, 
                            algorithm)
                    else:
                        standalone_decrypt(
                            filename, 
                            key, 
                            algorithm)
                else:
                    print("Invalid parameters. \n" + help_message)
            except Exception as e:
                print(e)
                print("Invalid parameters. \n" + help_message)

        elif method_id == "2": # random number
            key = sys.argv[0]
            test_randomness = False
            if nb_args == 3:
                test_randomness = True if sys.argv[1] == "True" else False

            rdm_generator = RandomNumberGenerator(key, use_custom=False)
            print(f"Your random number: {rdm_generator.generate()}")
            if test_randomness:
                rdm_generator.display_random_image()
                rdm_generator.verify_randomness()
                rdm_generator.plot_random_and_semi_random()

        elif method_id == "3": # full cipher/decipher pipeline            
            filename = sys.argv[0]
            algorithm = sys.argv[1] if sys.argv[1] == "rc4" or sys.argv[1] == "rc5" else None
            key = sys.argv[2]

            WAV_file_demo = False
            if nb_args == 5:
                WAV_file_demo = True if sys.argv[3] == "True" else False
                if WAV_file_demo and not filename.split(".")[-1] == "wav":
                    print("Parameter 'WAV_file_demo' is only for WAV files. Parameter ignored.")
                    WAV_file_demo = False
            
            encrypt_decrypt_and_compare(
                filename, 
                key, 
                algorithm,
                is_creating_wav_demo_file=WAV_file_demo)
        exit()

    else: # invalid method id
        print("Invalid method id. \n" + help_message)