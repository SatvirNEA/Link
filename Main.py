import Contacts        # Importing required modules/files
import Encryption       
import socket
import threading
import Algorithms

# socket library is used to send data packets from one computer to another as well as giving 
# the ability to close connections
# When sending data, all packets are encoding using UTF-8 encoding, hence the 'utf-8' with every send function

# threading library allows for the code to utilise threading, and have multiple functions within the code
# running simulatenously. This allows for messages to be sent by client and received at the same time


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Sockets():
    def __init__(self):
        self.__host = str()     # Set private and public attributes
        self.__port = int()
        self.name = str()
        self.publickey = []
        self.privatekey = []
        self.userID = str()
        self.stop = False
        self.keyswork = False

    def sethost(self, host):       # Getters and Setters
        self.__host = host

    def gethost(self):
        return self.__host

    def setport(self):
        self.__port = 5555      # Sets port, which is used in UserIDs

    def getport(self):
        return self.__port

    def setname(self):
        done = False
        while not done:
            name = str(input("\nEnter Your Display Name :> "))
            presence = Algorithms.presencecheck(name, "Name")       # Input validation
            length = Algorithms.lengthcheck(name, 3, 25, "Name")
            formatted = Algorithms.formatcheck(name, "Name")

            if length and presence and formatted:       
                done = True

        self.name = name    # Updates attribute

    def genkeys(self):
        self.publickey, self.privatekey = Encryption.generatekeys()     
        # Calls Encryption file, generating key pair, and updates attributes

    def getuserID(self):
        self.userID = Algorithms.createID(self.__host, self.__port) 
        # Calls createID function in Algorithms file
    
    def restart(self):
        ContactsTree =  Contacts.initialsecontacts(self.userID)    
        # Calls Contacts Code, and creates binary tree from hash table saved
        Algorithms.printlogo()  
        MainMenu(ContactsTree)      # Prints Main Menu for a restart

        # Above function is called when a client has been disconnected from server for a number of reasons
        # or when the server has decided to end the chat


    def receive(self, client):      # Receive messages function used by client 
        while True and not self.stop:     # Always runs in the background due to it being started in a threa
            if self.stop:      # Closes thread once a connection is lost 
                break

            try:        # Exception handling, in case the server goes down
                if not self.stop:
                    message = client.recv(4096).decode('utf-8')     
                    # Receive message from server, using socket library and decodes it using UTF-8 decoder

                    if message == 'NAMEREQ':  # Send's client name if requested   
                        client.send(bytes(self.name, "utf-8"))  # Uses socket library to send name

                    elif message == 'KEYREQ':   # If message received from server is KEYREQ, begin a key exchange
                        serverkey = self.keyexchange(client)    
                        self.serverkey = [int(x) for x in serverkey.split('|')] 
                        # Formats server's publickey so it can be used correctly
            
                    elif message == "FULL":     # If server sends back that the chat is full 
                        print("[ERROR --> Chat is full!]")  # Displays error to user
                        client.close()      # Uses socket library to close connection

                        # This is triggered when there are 4 clients connected to the server

                    elif message == "KICK {}".format(self.name):    # Alerts User If they have been kicked
                        print("You Have Been Kicked From The Server\nPlease Press Enter ")

                    else:   # If message recieved is not a reqeust for Name or Key 
                        message = Encryption.decrypt(message, self.privatekey)
                        print(message) 

                        # Calls encryption file and uses the client privatekey in order to decrypt message
                        # Prints message to user after decryption 


            except:     # If there is an error server side and a message isn't received
                self.stop = True    # Allows threads to end
                client.close()    # Disconnects Client and then ends all subroutines
                dummyvar = str(input("You Have Been Disconnected\nPress Enter To Leave "))  
                # Prevents wrong input for menu when it is run

                self.restart()     

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ClientSocket(Sockets):    # Class for clients who connect to the server
    def __init__(self):     # Initialises attributes and creates serverkey attribute
        Sockets.__init__(self)
        self.serverkey = [int()]        # Serverkey is a list [used as list for encrpytion and decryption]

    def keyexchange(self, client):      # Key exchange sequence for client side
        string = str("")        

        # In key exchanges, the client will send their publickey first, and 
        # will then receive the publickey of the server

        for char in range(len(Algorithms.allchars)):
            string += Algorithms.allchars[char]     # Creates a string with all the allowed characters 

        done = False
        while not done:  
            try:
                message = Encryption.encrypt(string, self.publickey)        
                # Encrypts string using their own public key
                
                client.send(bytes(message, "utf-8"))        
                # Attempts to send this to the server, using socket library
                
                key = str(self.publickey[0]) + '|' + str(self.publickey[1])     
               
                # If successuly sent without error, key is then prepared to be sent
               
                client.send(bytes(key, "utf-8"))        # Key is sent 
                done = True     # Breaks the loop, as the keys are valid and have been sent

            except:
                self.genkeys()  
                # If there is a surrogate error, new keys are generated and key exchange is tried again

        # Above loop is done in order to prevent a surrogate error bug that kept occuring
        # If a surrogate error occurs, new keys are generated and checked for any surrogate errors
                
        done = False
        while not done:
            message = client.recv(4096).decode("utf-8")     
            # Receives encrypted string of all allowed characters
            
            serverkey = client.recv(4096).decode("utf-8")   
            # Receives the publickey of the server
            
            done = True 

        return serverkey  # Key exchange has been completed

    def send(self, client):
        while True and not self.stop:     # Always runs in the background due to it being started in a thread            
            try:
                string = str(input("\n"))   # Takes input of user
                
                if self.stop:       # Closes thread once a connection is lost
                    break
                
                if string.lower() == "/quit":  
                    client.close()  # Uses sockets library to close connection

                CTS = Algorithms.messagecheck(string)

                if CTS:
                    message = "[{}]:> {}\n".format(self.name, string)    
                    # Creates message, joining the user's name to it in order for others to identify it

                    message = Encryption.encrypt(message, self.serverkey)  
                    # Calls Encryption file in order to encrypt the message
                    
                    client.send(bytes(message, "utf-8"))      
                    # Sends the encrypted message, and it is encoded using the utf8 codec
                
                else:   # If input validation fails
                    pass

            except:     # If there is an error [i.e Connection lost]
                break   # Breaks from loop and thread is closed

    def start(self):
        self.stop = False    # Used to break threads, setting to true ensures no errors at startup
        self.setname()       # Sets name to use
        self.genkeys()       # Generates Keys
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates socket
        self.userID = input("Enter UserID of Person You Want To Connect To :> ") 
        
        # Gets UserID of server that the User wishes to connect to

        host, port = Algorithms.gethost(self.userID)    
        client.connect((host,port))     
        
        # Binds host and port, then connects to the 'client'
        # In this case the 'client' is actually the server

        receivemessages = threading.Thread(target = self.receive, args = (client,))  
        receivemessages.start()
        
        sendmessages = threading.Thread(target = self.send, args = (client,))
        sendmessages.start()

        # Uses threading in order to allow receiving of messages and sending of messages at the same time

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ServerSocket(Sockets):    # Class for Server 
    def __init__(self):         # Set attributes / inherits sockets class
        Sockets.__init__(self)
        self.clients = []       # Stores client's information
        self.client = ""
        self.server = ""
        
    def keyexchange(self, client):      # Key exchange sequence for server side
        string = str("")

        # In key exchanges, the client will send their publickey first, and 
        # will then receive the publickey of the server

        for char in range(len(Algorithms.allchars)):    # Creates a string with all the allowed characters
            string += Algorithms.allchars[char]

        client.send(bytes("KEYREQ", "utf-8"))   # Alerts the client to initiate key exchange

        done = False
        while not done:
            message = client.recv(4096).decode("utf-8")     # Receives encrypted string of all allowed characters
            clientkey = client.recv(4096).decode("utf-8")   # Receives the publickey of the client
            done = True

        done = False
        while not done:
            try:
                message = Encryption.encrypt(string, self.publickey)    # Encrypts string using their own public key
                client.send(bytes(message, "utf-8"))     # Attempts to send this to the client

                key = str(self.publickey[0]) + '|' + str(self.publickey[1]) 
                
                # If successuly sent without error, key is then prepared to be sent
                
                client.send(bytes(key, "utf-8"))    # Key is sent 
                done = True     # Breaks the loop, as the keys are valid and have been sent

            except:
                self.genkeys()   
                # If there is a surrogate error, new keys are generated and key exchange is tried again

        # Above loop is done in order to prevent a surrogate error bug that kept occuring
        # If a surrogate error occurs, new keys are generated and checked for any surrogate errors

        return clientkey    # Key Exchange has been completed

    def send(self, message):
        originalmessage = message   # Sets the original message so that it is not changed

        print("\n{}".format(originalmessage))

        for index in range(0, len(self.clients)):   # For each client
            self.client = self.clients[index][0]    # Gets client info
            self.key = self.clients[index][2]       # Gets the public key for this client

            message = Encryption.encrypt(originalmessage, self.key)     
            # Encrypts the original message using the key for the corresponding client

            try:
                self.client.send(bytes((message), "utf-8"))      # Sends the encrypted message
            
            except:     # If there is an error, message is not sent
                pass

    def closeconnection(self, client):
        try:
            client.close()  # Closes connection with the client
            index = Algorithms.linearsearch3D(client, self.clients, 0)     
            # Gets index of where client's information is stored, using linear search
            
            name = self.clients[index][1]
            self.clients.pop(index)     # Removes client's information from the array
            message = '\n[{} HAS LEFT]\n'.format(name)    # Creates a message showing who has left
            self.send(message)  # Sends the message to each client and breaks out of loop
        
        except:
            pass

    def handle(self, client):   # Handles a client after they have connected
        while True:     # Always runs in the background due to the thread
            try:        # Exception handling in case one of the clients leaves
                message = client.recv(4096).decode('utf8')  # Receives any message sent to the server
                # 4096 refers to buffer size
                message = Encryption.decrypt(message, self.privatekey)   
                # Decrypts the message using the server's private key
                self.send(message) # Sends message to all the clients
            
            except:     # If the client is no longer connected, or an error has occured
                self.closeconnection(client) # Closes connection with client
                break

    def handlecommands(self, message):
        if message[len(self.name) + 5:].lower().startswith("/kick"):     # If the message starts with /kick
            print("")  
            for x in range(len(self.clients)):      # Prints each client
                print("{} - {}".format((x + 1), self.clients[x][1]))
    
            index = str(input("\nEnter A Number For Who You Would Like Kicked :> "))     
            # User chooses who to kick

            try:
                index = int(index) - 1      
                # Input Validation [If input cannot be converted to integer, it is wrong]

                self.clients[index][0].send(bytes("KICK {}".format(self.clients[index][1]), "utf-8"))    
                # Sends the client a notification to let them know they have been kicked
                self.clients[index][0].close()  # Closes connection

            except:
                print("\nERROR --> Invalid Number\n")    # Input validation
        
        elif message[len(self.name) + 5:].lower().startswith("/quit"):     # If user wants to quit
            self.stop = True    # Allows some threads to break
            for index in range(len(self.clients)):  
                self.clients[index][0].close()      # Linearly closes connection with each client
            
            print("\nClosed All Connections")   
            dummyvar = str(input("Press Enter To Continue "))   # Allows program to be restarted
            self.restart()

    def sendmessages(self):
        while True:     # Always runs due to being in a thread
            try:
                if len(self.clients) != 0:
                    string = str(input("\n"))
                    CTS = Algorithms.messagecheck(string)

                    if CTS:
                        message = "[{}]:> {}\n".format(self.name, string)       
                        # Allows server to send messages to clients

                        if message[len(self.name) + 5:].startswith("/"):        
                            # Calls procedure to deal with commands
                            self.handlecommands(message)

                        else:
                            self.send(message)      
                            # Sends message to all clients, if message is not a command
                    
                    else:
                        pass
                    
            except:
                print("\n[ERROR --> Connection Lost]")  # If there is an error
                for index in range(len(self.clients)):  
                    self.closeconnection(self.clients[index][0])    # Closes connection with all clients


    def receive(self):      # Overridden Method from Sockets Class
        while True:     # Always runs in the background due to the thread
            try:

                self.client , address = self.server.accept()     
                # Server accepts connections, and takes the client information and Private IP Address

                if len(self.clients) == 4:      
                    # Restricts number of users in a chat to 5 (including the server hoster) 
                    print("[ERROR --> Someone Tried To Join While Server Is Full!]\n")
                    self.client.send(bytes("FULL", "utf-8"))    # Alerts client that chat is full
                    self.client.close()     

                else:
                    clientID = Algorithms.createID(str(address[0]), self.getport())
                    # Gets client UserID based on connected IP Address
                    
                    self.client.send(bytes('NAMEREQ', "utf8"))      
                    # Sends the newly connected client a request to get their name
                    
                    clientname = str(self.client.recv(4096).decode('utf8'))  # Receives the name of client
                    
                    clientkey = self.keyexchange(self.client)   # Initiates key exchange
                    clientkey = [int(x) for x in clientkey.split('|')] # Formats client's publickey

                    self.clients.append([self.client, clientname, clientkey, clientID])        
                    # Adds the connected client's information 

                    message = ("\n[{} JOINED]\n ".format(clientname))   
                    # Sets a message to be sent to all clients already connected   
                    self.send(message)      # Calls the send function, sending the message and clients array

                    sending = threading.Thread(target = self.sendmessages)      # Sets threads and runs them
                    sending.start()                                     

                    handleclient = threading.Thread(target = self.handle, args = (self.client, )) 
                    handleclient.start()
                    # These threads allow server to handle clients and send messages simultaneously
            
            except:
                pass
        
    def start(self):
        # self.stop = False   # Used to break threads, setting to false ensures no errors at startup
        self.setname()
        self.sethost(socket.gethostbyname(socket.gethostname()))        # Gets the Private IP of the machine the server is running on
        self.setport()     # Set port and get UserID
        self.getuserID()
        print("UserID :> {}".format(self.userID))

        self.genkeys()      # Generate server's keypair
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Creates Server socket
        self.server.bind((self.gethost(), self.getport()))       # Binds the host and port to the Server Socket
        self.server.listen()        # Server 'listens' for connections

        receivemessages = threading.Thread(target = self.receive)
        receivemessages.start()     # Starts thread that runs the receive function in the background

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def MainMenu(ContactsTree):     # Menu Function
    choice = Algorithms.menu()

    if choice == "1":
        serversock = ServerSocket() # Creates object for server
        serversock.start()  # Starts server

    elif choice == "2":
        clientsock = ClientSocket() # Creates object for client
        clientsock.start()  # Starts client

    elif choice == "3":     # Runs Contacts Menu
        ContactsMenu(ContactsTree)  

def ContactsMenu(ContactsTree): 
    done = False
    while not done:
        choice = Algorithms.ContactsMenu()

        if choice == "1":
            ContactsTree.viewcontacts()
            # Calls method for in order tree traversal 
        
        elif choice == "2":
            Contacts.addcontact(ContactsTree)   # Calls contacts file to add a contact
        
        elif choice == "3":
            ContactsTree = Contacts.deletecontact(Algorithms.createID(socket.gethostbyname(socket.gethostname()), 5555), ContactsTree)
            # Calls method to delete a contact

        elif choice == "4":
            Contacts.searchforcontact()
            # Calls contact file to search for a contact
        
        elif choice == "5":
            done = True # Allows user to travel back from Contacts Menu to Main Menu
    
    MainMenu(ContactsTree)  

ContactsTree = Contacts.initialsecontacts(Algorithms.createID(socket.gethostbyname(socket.gethostname()), 5555))
Algorithms.printlogo()
MainMenu(ContactsTree)

# Creates inital object for Contacts Binary Tree and then prints menu and starts the program