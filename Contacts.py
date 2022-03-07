import Algorithms   # Imports algoritms file
import time     # Imports time which allows the program to wait a number of seconds before continuing

class Tree:         # Binary Tree for Contacts 
    def __init__(self, node):
        self.node = node        # Creates node, with child nodes left and right set to none
        self.left = None
        self.right = None

    def writetofile(self, node):
        file = open("Contacts.txt", "r+")    # Opens in read and write mode
        lines = file.readlines()    # Reads all lines
        file.close()    # Closes file
        chars = Algorithms.getchars(node[0])    # Gets all characters from inputted contact name
        
        index = Algorithms.hashcontact(chars)   # Gets index for hash table

        done = False
        while not done:
            if lines[index] == "\n":    # If index is empty space
                lines[index] = "{}|{}\n".format(node[0], node[1])   # Writes contact to file in index
                done = True

            else:
                index += 1  # Checks for next available space if space is taken

            if index == 99:    # Checks start of file [if space is only available behind hashed index val]
                index = 0   


        file = open("Contacts.txt", "w+")   # Opens in write mode 
        file.writelines(lines)  # Writes to file
        file.close()    # Closes file

    def add(self, node, append):
        if self.node:   # If current node is occupied

            if node[0] > self.node[0]:      # Alphabetically compares name of contact to be added with current node
                if self.right == None:          # If there is no right child
                    self.right = Tree(node)     # Creates node at right child with the contact
                
                else:       # If right child is occupied
                    self.right.add(node, False)        # Recursive call, which travels to occupied right node
            
            elif node[0] < self.node[0]:    # Left Child checked in this instance
                if self.left == None:       # If there is no left child
                    self.left = Tree(node)      # Creates node at left child with the contact
                
                else:       # If left child is occupied
                    self.left.add(node, False)     # Recursive call, which travels to occupied left node
        
        else:       # If current node is not occupied (free space)
            self.node = node    # Contact is added to this node
        
        if append:
            self.writetofile(node)

    def viewcontacts(self):     # In order Traversal
        if self.left:      # If left node exists
            self.left.viewcontacts()        # Recursive call, which travels to occupied left node
        
        print("""                          
Contact Name : {}  
UserID       : {} """.format(self.node[0], self.node[1]))       # Once leftmost node is travelled to, it is printed


        if self.right:      # After leftmost node is checked, the right nodes are then checked
            self.right.viewcontacts()       # Recursive call

def initialsecontacts(userID):      # Run when main program starts
    try:
        file = open("Contacts.txt", "r+")

    except:
        file = open("Contacts.txt", "w+")
    
    lines = file.readlines()       # Creates lines array, with all the lines in the text file
    
    if len(lines) == 0:     # If file is empty [no contacts saved]
        file.write("Me|{}\n".format(userID))    # Writes current userID

    elif lines[0] != "Me|{}\n".format(userID): # If first line is not correct
        lines[0] = "Me|{}\n".format(userID)     # Changes first line
        file.writelines(lines)      # Writes changes to file
    
    if len(lines) < 100:    
        for x in range(len(lines) - 1, 100):    # If any lines are deleted by user, they are replaces with empty lines
            file.write("\n")

    file.close()

    ContactsTree = Tree(["Me", userID])     # Creates binary tree, with user as root node

    if len(lines) > 1:      # If more than one contact is saved to file
        file = open("Contacts.txt", "r+")
        lines = file.readlines()
        file.close()
        for index in range(1, 100):      # For each line
            if lines[index] != "\n":
                node = [str(x) for x in (lines[index][:-1].split('|'))]     # Creates list with 1st index as name and 2nd index as userID
                ContactsTree.add(node, False)      # Adds each contact to the tree
    
    return ContactsTree
    
def deletecontact(userID, ContactsTree):
    name = validateinfo("Contact Name")     # Input validation
    chars = Algorithms.getchars(name)   # Gets chars for name

    index = Algorithms.hashcontact(chars)   # Performs hash on name
    originalindex = index

    file = open("Contacts.txt", "r+")   # Opens file in read/write mode
    lines = file.readlines()    # Reads all lines
    file.close()    # Closes file

    done = False
    deleted = False
    count = 0

    while not done and count < 2:   # Creates loop 
        if lines[index] != "\n":    # If line is not empty
            Contact = [str(x) for x in (lines[index][:-1].split('|'))]  # Gets contact name by removing user ID and |
            if Contact[0] == name:  # If contact is same name
                lines[index] = "\n" # Replaces with empty line
                deleted = True  
                done = True

        if index == originalindex:     # Prevents infinite loop 
            count += 1

        index += 1
    
        if index == 99:    # Checks start of file [if added behind hashed index val]
            index = 0

    if deleted:     # If a contact was deleted, contacts are reinitialised
        file = open("Contacts.txt", "w+")
        file.writelines(lines)
        file.close()
        ContactsTree = initialsecontacts(userID)
        print("\nDeleted {} From Contacts\n".format(name)) # Lets user know that Contact has been deleted
        time.sleep(1) 
    
    else:
        print("\nERROR --> Name Entered is not a Contact")  # If no contact was deleted, the name was wrong
        time.sleep(1)

    return ContactsTree

def validateinfo(inputtype):    # Input Validation
    done = False
    while not done:
        data = str(input("\nEnter {} :> ".format(inputtype)))
        
        if inputtype == "Contact Name":
            length = Algorithms.lengthcheck(data, 3, 25, inputtype)
            formatted = Algorithms.formatcheck(data, inputtype)

        presence = Algorithms.presencecheck(data, inputtype)

        if inputtype == "Contact Name":
            if length and formatted and presence:
                done = True

        else:
            if presence:
                done = True
    return data

def pushtostack(stack, pointer, data):  # Pushes to stack
    if data != "\n":    
        stack[pointer] = data
        pointer += 1

    return stack, pointer


def checkforduplicates(name):
    file = open("Contacts.txt", "r+")    # Opens in read mode
    lines = file.read().splitlines()    # Reads every line and splits the new lines
    for line in range(len(lines)):
        contact = [str(x) for x in (lines[line][:-1].split('|'))]   # Contact saved as list with the Name in index 0 and userID in index 1
        if contact[0] == name:  # If duplicate, check is not passed
            print("ERROR --> Contact With This Name Is Already Saved\n")
            time.sleep(1)
            return False

    return True     # Check passed if no duplicates found

def addcontact(ContactsTree):       
    file = open("Contacts.txt", "r+")
    lines = file.readlines()        # Reads all lines 

    stack = [None] * 100
    pointer = 0
    for line in range(len(lines)):  # Adds contacts to stack
        stack, pointer = pushtostack(stack, pointer, lines[line])

    if pointer == 100:  # If pointer is at top of stack, contacts are full
        print("ERROR --> Contacts Full\n")      
        time.sleep(1)

    else:
        full = False

    done = False
    while not done and not full:
        name = validateinfo("Contact Name")     # Input validation
        userID = validateinfo("Contact UserID") 
        done = checkforduplicates(name)

    ContactsTree.add([name,userID], True)       # Adds Contact to binary tree
    
    
def searchforcontact():
    file = open("Contacts.txt", "r+")
    lines = file.readlines()        # Reads contacts file
    file.close()    
    name = validateinfo("Contact Name") # Gets name and does input validation
    chars = Algorithms.getchars(name)

    index = Algorithms.hashcontact(chars)       # Hashes name in order to look in hash table

    originalindex = index       
    count = 0
    found = False
    done = False

    while not done and count < 2:       # Count < 2 prevents infinite loop
        if lines[index] != "\n":
            Contact = [str(x) for x in (lines[index][:-1].split('|'))]      # Formats to have just contact name
            if Contact[0] == name:  # If Contact is found
                print("""
SEARCH RESULT

Contact Name : {}  
UserID       : {} """.format(Contact[0], Contact[1]))       

                time.sleep(1)
                found = True
                done = True

        if index == originalindex:     
            count += 1

        index += 1
    
        if index == 100:    # Checks start of file [if added behind hashed index val]
            index = 0
    
    if not found:
        print("\nERROR --> No Contact Saved With The Name {}".format(name)) 
        time.sleep(1)
