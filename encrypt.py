'''
This is a module to encrypt / decrypt strings using plaintext files as storage
'''
from cryptography.fernet import Fernet

keyFileName = '.key_secret'
encodedFileName = '.encoded_secret'

def save(fileName,data):
    '''
    Store binary data in fileName
    '''
    file = open(fileName,'wb')
    file.write(data)
    file.close()

def encryptAndSaveString(string):
    '''
    generate_key, encrypt string, save key and encrypted string in files
    '''
    # generate and store key
    key = Fernet.generate_key()
    save(keyFileName,key)

    # convert string to binary and encrypt
    cipher_suite = Fernet(key)
    encodedString = cipher_suite.encrypt(string.encode())

    save(encodedFileName,encodedString)

def load(fileName):
    '''
    load binary data from fileName
    '''
    file = open(fileName,'rb')
    data = file.read()
    file.close()
    return data

def loadAndDecryptString():
    '''
    load key and encrypted string, decrypt string
    '''
    encodedString = load(encodedFileName) # get encoded string from file
    key           = load(keyFileName)     # get key from file

    cipher_suite = Fernet(key)
    string = cipher_suite.decrypt(encodedString).decode()
    return string

if __name__ == '__main__':
    string = input('inupt string to secure: ')
    encryptAndSaveString(string)
    result = loadAndDecryptString()
    print(result)
    if string == result:
        print('match - encrypt-decrypt cycle successful')
    else:
        print('failure - original does not match decoded')
