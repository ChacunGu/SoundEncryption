"""
Security course
Chacun Guillaume, Feuillade Julien
HE-Arc, Neuchâtel
2018-2019

***

rc4.py
"""

import array 

MOD = 256

def KSA(key):
    """
    Key-scheduling algorithm from pseudo-code of Wikipedia
    """
    key_length = len(key)
    tab = list(range(MOD))
    j = 0
    for i in range(MOD):
        j = (j + tab[i] + key[i % key_length]) % MOD
        tab[i], tab[j] = tab[j], tab[i]
    return tab


def PRGA(tab):
    """
    Pseudo-random generation algorithm form pseudo-code of Wikipedia
    """
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + tab[i]) % MOD

        tab[i], tab[j] = tab[j], tab[i]
        K = tab[(tab[i] + tab[j]) % MOD]
        yield K


def KeyStream(key):
    """
    Put the two function together to get the key stream
    """
    keyKsa= KSA(key)
    return PRGA(keyKsa)


def logic(key, byteArray):
    """
    Logic of the encryption, encryption key used for encrypting
    """
    key = [ord(c) for c in key]
    keystream = KeyStream(key)

    result = []
    for c in byteArray:
        value = (c ^ next(keystream))
        result.append(value)
    return result


def encrypt(key, byteArray):
    return logic(key, byteArray)


def decrypt(key, cipher):
    """
    Use codecs library to decode the cipher
    """
    result = logic(key, cipher)
    return array.array("B", result)