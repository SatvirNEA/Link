import time   # Imports time which allows the program to wait a number of seconds before continuing

allowedchars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", 
"p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", "0", "1", "2", "3", "4", "5", 
"6", "7", "8", "9", "!", "@", "#","£", "$", "%", "^", "&", "*", "(", ")", "-", "=", "_", "+", 
"[", "]", ";", "'", ":", '"', "<", ">", ",", ".", "/", "?"
]


allchars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "O", "P", "Q",
"R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
"k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", "0", "1",
"2", "3", "4", "5", "6", "7", "8", "9", "!", "@", "#", "£", "$", "%", "^", "&", "*", "(", ")", "-", 
"=", "_", "+", "[", "]", ";", "'", ":", '"', "<", ">", ",", ".", "/", "?"
]

# Sets allowed characters (allowedchars is same as allchars, but doesn't contain capital letters)

def getchars(string):       
    return [char for char in string]        # Returns a list, where each element is each 'letter' of a string

def linearsearch(item, searchlist, returnval):
    for index in range(len(searchlist)):    # Checks each item in the list
        if searchlist[index] == item:       # If the searched item is the item being looked for, return True

            if returnval == "Present":
                return True

            if returnval == "Index":
                return index  

    return False        # False is returned if the search is unsucessful 

def linearsearch3D(item,searchlist,x):
    for index in range(0, len(searchlist)):        # Checks each item in the list
        if str(searchlist[index][x]) == str(item):        # If searched item is the item being looked for, returns index
            return index                        # Only checks first element of each list within the main list (this function is for specific use)

    return False        # False is returned if search is unsuccessful

def presencecheck(string, text):
    if string != "":    # If string is not empty, check is passed
        return True

    else:
        print("\nERROR --> {} Cannot Be Blank".format(text))
        return False

def lengthcheck(string, lower, upper, text):
    chars = getchars(string)        # Gets characters

    if len(chars) >= lower and len(chars) <= upper:     # len(chars) signifies amount of characters in string
        return True      # If number of characters is within accepted length, the check is passed

    else:       # If outside range, check is not passed
        print("\nERROR --> {} must be between {} and {} characters".format(text, lower, upper))
        return False

def formatcheck(string, text):
    chars = getchars(string)        # Gets characters

    for index in range(len(chars)):
        found = linearsearch(chars[index].lower(), allowedchars, "Present") 
        # If the character is a letter, it is passed to linear search as it's lowercase character
        # This saves time when searching for it, as both capital and lower case letters would not have to be checked
        
        if not found:      
            print("\nERROR --> {} Contains Disallowed Character '{}'".format(text, chars[index]))
            return False

    return True     # If found, check is passed

def messagecheck(message):  # Used to check if a message is valid to send [Input Validation]
    presence = presencecheck(message, "Message")
    length = lengthcheck(message, 3, 100, "Message")
    formatted = formatcheck(message, "Message")

    if presence and length and formatted:
        return True
    
    else:
        return False

def printlogo():
    print("""                              
██╗     ██╗███╗   ██╗██╗  ██╗   
██║     ██║████╗  ██║██║ ██╔╝  
██║     ██║██╔██╗ ██║█████╔╝  
██║     ██║██║╚██╗██║██╔═██╗   
███████╗██║██║ ╚████║██║  ██╗  
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝  """)

    time.sleep(1)

def loadingbar(text, interval):     # Animation used when quitting
    for x in range(0, 30):
        string = text + " [" + ("#" * x) + ("-" * (29 - x) + "]")       
        print(string, end="\r")
        time.sleep(interval)
    print("")

def ContactsMenu(): 
    print("""
----------------
|   CONTACTS   |
----------------

1. View All Contacts
2. Add Contact
3. Delete Contact
4. Search For Contact
5. Back""")

    time.sleep(1)

    done = False
    while not done:
        choice = str(input("\nEnter A Choice [1 - 5] :> "))

        if linearsearch(choice, ["1", "2", "3", "4", "5"], "Present"):      # Input validation
            return choice
        
        else:
            print("INVAID --> Enter Valid Choice")

def menu():
    done = False
    print("""
-----------------
|   MAIN MENU   |
-----------------

1. Start Server
2. Connect To Server
3. Contacts Menu
4. Quit""")

    time.sleep(1)
    while not done:
        choice = str(input("\nEnter A Choice [1 - 4] :> "))

        if linearsearch(choice, ["1", "2", "3"], "Present"):        # Input validation
            return choice

        elif choice == "4":
            loadingbar("QUTTING", 0.01)
            done = True

        else:
            print("INVAID --> Enter Valid Choice")

def hashcontact(chars):
    val = 0
    for index in range(len(chars)):
        val += linearsearch(chars[index], allchars, "Index")

    index = val % 100
    return index


def createID(host, port):         # This function takes the private IP of the user and returns a unique ID for that IP
    chars = getchars(host)      # Calls function that returns a list containing each part of the IP
    userID = ""         # Initialises the userid string
    num = ""            # Temporary store of numbers
    numlist = []        # List of complete numbers in IP (e.g in '192.168.0.1' it would store 192, 168, 0, 1)

    for char in chars:      # For each character in the IP
        if char != ".":     # If it's a number
            num += char     # Adds the single digit number to the num string

        else:       # If the character is a '.'      
            numlist.append(num)     # Adds the number before the '.' into the numlist
            num = ""    # Resets num, so that the new number can be detected after the '.'

    numlist.append(num)     # Adds the last number into the numlist, since the for loop breaks before it does so 

    for num in numlist:     # For each number
        num = (int(num) * 2) + 10     # Multiply the number by 2 and then add 10
        userID += str(num)      # Adds the final number to the string of the userID
        userID += "-"           # Adds a dash after each number

    userID+= str(port)
    return userID

def gethost(userID):            # Works same way as above function, but reverses the process
    chars = getchars(userID)
    host = ""
    num = ""
    numlist = []
    count = 0

    while count < 4:
        for char in chars:
            if char != "-":
                num += char

            else:
                numlist.append(num)
                count += 1
                num = ""

    port = ""
    for index in range((len(chars) - 4), len(chars)):
        port+= str(chars[index])

    count = 0
    for num in numlist:
        num = int(num) - 10     # Subtracts 10 and then divides by 2
        num = num // 2
        host += str(num)

        count  += 1
        if count != len(numlist):
            host += '.'

    return host, int(port)

    