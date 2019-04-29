# SoundEncryption
## Principle
Sound encryption and decryption using block and stream ciphers.

## Context
Project developed in Python for the Security course of the 3rd year orientation "DLM" at HE-Arc.

Haute École Arc Ingénierie, Neuchâtel, Suisse. 2018/19

## How to use
This projet has been tested with Python 3.7.3 (64bit).

Please install the Python modules from the requirements.txt file !

### Available methods

#### Help
`python SoundEncryption.py`

Displays the application's help message describing the available methods.

#### Method n°1: cipher/decipher
`python SoundEncryption.py 1 mode filename algorithm key`

Cipher or decipher specified file using specified algorithm & key.

- mode: "cipher" or "decipher" depending on which operation you want to do
- filename: the file you want to encrypt or decrypt
- algorithm: "rc4" or "rc5" depending on which algorithm you want to use
- key: the key you want to give to the selected algorithm

#### Method n°2: pseudo-random
`python SoundEncryption.py 2 key test_randomness`

Generate a pseudo-random number with RC4 algorithm initialized with given key. Displays proof of randomness if parameter 'test_randomness' is set to True.

- key: the key you want to give to RC4 algorithm
- *test_randomness: optional parameter "True" or "False" depending if you want to display the proof of randomness*

#### Method n°3: complete pipeline
`python SoundEncryption.py 3 filename algorithm key WAV_file_demo`

Cipher then deciphers and compare data to verify ciphering and deciphering operations were successful. If processing a .WAV file parameter 'WAV_file_demo' allows to create a listenable version of the ciphered file.

- filename: the file you want to encrypt or decrypt
- algorithm: "rc4" or "rc5" depending on which algorithm you want to use
- key: the key you want to give to the selected algorithm
- *WAV_file_demo: optional parameter "True" of "False" depending if you cipher/decipher a .WAV file and you want to be able to listen the ciphered file*

### Listenable ciphered WAV file restrictions
For the 3rd method we are using Python's wave library to read WAV files header. However as of today it only supports specific subcategory of .WAV file format (WAVE_FORMAT_PCM: 0x0001). Don't worry if you are trying to read an unsuported .WAV file the application will tell you. Of course you can always set the flag "WAV_file_demo" to "False" and still observe that the output file is identic as the source.

### Customized RC4
If you want to try our customized RC4 method the flag USE_CUSTOM_RC4 in the main of the file SoundEncryption.py can be set to "True" (default value is "False").

## Team members
  * [Chacun Guillaume](https://github.com/ChacunGu)
  * [Feuillade Julien](https://github.com/Royejul)
