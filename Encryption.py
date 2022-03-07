import random   # Imports random library and GenPrimes file
import GenPrimes

def getprimes():    
    while True:     # Keeps looping 
        rand1 = random.randint(1,125)   # Generates two random numbers
        rand2 = random.randint(1,125)      
        if rand1 != rand2:      
            primefile = open("Primes.txt" , "r")
            lines = primefile.readlines()   # Reads Primes text file
            m = (lines[rand1 - 1])  # Chooses two random prinme numbers
            m = int(m[:-1])     # Removes "\n" from line
            n = (lines[rand2 - 1])
            n = int(n[:-1])
            primefile.close()   # Closes file
            return m,n          # Returns two random numbers

def modinverse(phi, x):     # Modular inverse function
    for y in range(1, x):   
        if (phi * y) % x == 1:  # Performs modular inverse
            return y
    return False    # If no mod inverse exists, false is returned


def highestdenom(phi , x):
    while x != 0:      # Allows for a continous loop until highest denominator is found
        temp = phi % x      # Finds mod
        phi = x     # Replaces phi with x 
        x = temp    # Is replaced with the mod
    return phi  # Once done, phi is returned

def getcoprimes(phi):   
    coprimes = []   # Creates coprimes list
    for x in range(2, phi):     # Loops up to phi
        if highestdenom(phi, x) == 1 and modinverse(x, phi) != False:   # IF mod inverse exist, and phi and x do not share a denominator
            coprimes.append(x)  # Adds to coprimes 

        if len(coprimes) > 5:   # Once 6 coprimes added
            break   # Breaks loop

    for x in (coprimes):        # For each coprime
        if x == modinverse(x, phi): # Mod inverse is worked out and compared to x
            coprimes.remove(x)         # If equal, it is removed

    return coprimes     # Returns coprimes list

def generatekeys():     # Function to generate keys
    GenPrimes.genprimes(691)    # Generates primes up to 691 [125th Prime]
    m , n = getprimes()     # Gets random primes
    z = m * n       # Multiplies
    phi = (m - 1) * (n - 1)     # Uses Carmichaels totient function

    
    e = random.choice(getcoprimes(phi))     # Gets random coprime
    d = modinverse(e, phi)  # Performs mod inverse of this with phi 

    publickey = [e, z]      # Sets public and private keys and returns them
    privatekey = [d, z]

    return publickey, privatekey


def encryptblock(m, e, z):  # Performs [(Message ^ e) MOD z] 
    c = (m**e) % z
    return c

def decryptblock(c, d, z):  # Performs [(Message ^ d) MOD z]
    m = (c**d) % z
    return m

def encrypt(string, public_key):    
    e, z = public_key   # Splits key into e and z
    return ''.join([chr(encryptblock(ord(x), e, z)) for x in list(string)]) 
    # Encrypts message using ordinal of each character in message with e and z 

def decrypt(string, private_key):
    d, z = private_key  # Splits key into d and z
    return ''.join([chr(decryptblock(ord(x), d, z)) for x in list(string)])
    # Decrypts message using ordinal of each character in message with d and z 
