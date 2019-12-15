
#!pip3 install ast
#!pip3 install codecs
#!pip3 install ecdsa
#!pip3 install hashlib
#!pip3 install pycryptodome
#!pip3 install requests

import ast
import codecs
import ecdsa
import hashlib
from Crypto.Hash import keccak
import requests

# Ethereum Lottery

def private_key_from_string(msg):
    '''
    Applies the SHA256 hash function to the input string which creates a cryptocurrency private key.
    '''
    
    private_key = hashlib.sha256(msg.encode()).hexdigest()
    return private_key

def public_key_from_private_key(private_key):
    '''
    Converts the private key to a public key.
    '''

    private_key_bytes = codecs.decode(private_key, 'hex')
    key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    public_key = codecs.encode(key_bytes, 'hex')
    return public_key

def address_from_public_key(public_key):
    '''
    Converts the public key to an Ethereum wallet address with checksum.
    '''

    public_key_bytes = codecs.decode(public_key, 'hex')
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key_bytes)
    keccak_digest = keccak_hash.hexdigest()
    # Take the last 20 bytes
    wallet_len = 40
    wallet = '0x' + keccak_digest[-wallet_len:]
    return wallet

def get_balance(url):
    '''
    Checks the balance of the Ethereum address using the Etherscan API. 
    If the balance is 0, you did not win.
    If the balance is nonzero, you win!
    '''
    
    try:
        response = requests.get(url)
        status = response.status_code
        if response.status_code == 200:
            response = response.text
            response = ast.literal_eval(response)
            balance = int(response['result'])
            return balance
        else:
            print('An error has occurred.')
    except:
        print('An error has occurred.')
    
def play():
    '''
    Asks the user for an input string.
    Converts the string to a private key, public key, wallet address, and then checks the balance of that address.
    Prints a win/lose statement along with wallet info (balance, address, and private key).
    Asks the user if they want to play again.
    '''

    print('Welcome to the Ethereum Lottery! \nYour chance of winning is about 1 in 10^70 (essentially zero), but don\'t let that stop you!')

    playing = True
    while playing:

        msg = input('\nSimply enter some text and hit Enter: ')
        private_key = private_key_from_string(msg)
        public_key = public_key_from_private_key(private_key)
        address = address_from_public_key(public_key)
        api_key = '7Z99TEIBCGR4H7ACKNBU41IUY9QJGTCA82'
        url = 'https://api.etherscan.io/api?module=account&action=balance&address=' + address + '&tag=latest&apikey=' + api_key
        balance = get_balance(url)
        
        if balance == 0:
            print("\nSorry, you lost...")
        else:
            print('Congratulations! You won!')
        print('\nWallet Information', '\nBalance: ' + str(balance), '\nAddress: ' + address, '\nPrivate Key: ' + private_key)

        again = input("\nWould you like to play again? Enter 'y' or 'n' ")

        if again and again[0].lower() == 'y':
            playing = True
            continue
        else:
            print('Thanks for playing!')
            break

if __name__ == '__main__':
	play()
