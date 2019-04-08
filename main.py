from rc4 import encrypt, decrypt
from rc5 import RC5
from ResourceHandler import ResourceHandler

import array


if __name__ == '__main__':

    key = 'Wddddddiki'

    cryptor = RC5(key)
    cryptor.mode = "CBC"

    FILENAME_SOURCE = "./resources/audio/hello_world.wav"
    # "./resources/images/goat.jpg"
    # "./resources/text/hello_world.txt"

    FILENAME_DESTINATION = "./resources/audio/hello_world_rewritten.wav"
    # "./resources/images/goat_rewritten.jpg"
    # "./resources/text/hello_world_rewritten.txt"

    # read source file
    music = ResourceHandler.read_as_bytes(FILENAME_SOURCE)

    print(bytes(music[:]))
    enc_str = cryptor.encrypt(bytes(music[:50]))
    print(enc_str)
    dec_str = cryptor.decrypt(enc_str)
    print(dec_str)
    if dec_str == bytes(music[:50]):
        print('\nGood')
    else:
        print('\nBad')


    print(len(music))

    #print(bytes[0])


    header = music[:127]

    print(header)
    bytes = music[127:]
    cipher = encrypt(key, bytes)

    cipherFile = array.array("B", header.tolist() + cipher)

    print(cipherFile[:127])
    # create destination file
    ResourceHandler.write_bytes_to_file(cipherFile, FILENAME_DESTINATION)

    decrypted = decrypt(key, cipher)
    decryptFile = array.array("B", header.tolist() + decrypted)

    ResourceHandler.write_bytes_to_file(decryptFile, "./resources/audio/hello_world_decrypted.wav")

    if music.tolist() == decrypted:
        print('\nGood')
    else:
        print('\nBad')