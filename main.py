from rc4 import encrypt, decrypt
from ResourceHandler import ResourceHandler

import array


if __name__ == '__main__':

    key = 'Wddddddiki'

    FILENAME_SOURCE = "./resources/audio/hello_world.wav"
    # "./resources/images/goat.jpg"
    # "./resources/text/hello_world.txt"

    FILENAME_DESTINATION = "./resources/audio/hello_world_rewritten.wav"
    # "./resources/images/goat_rewritten.jpg"
    # "./resources/text/hello_world_rewritten.txt"

    # read source file
    bytes = ResourceHandler.read_as_bytes(FILENAME_SOURCE)

    print(len(bytes))

    #print(bytes[0])


    header = bytes[:45]

    print(header)
    bytes = bytes[45:]
    cipher = encrypt(key, bytes)

    cipherFile = array.array("B", header.tolist() + cipher)

    print(cipherFile[:45])
    # create destination file
    ResourceHandler.write_bytes_to_file(cipherFile, FILENAME_DESTINATION)

    print(bytes[:10])
    print(cipher[:10])

    decrypted = decrypt(key, cipher)
    print(decrypted[:10])

    if bytes.tolist() == decrypted:
        print('\nGood')
    else:
        print('\nBad')