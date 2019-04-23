import socket
import sys
from pydes import des

def Main():
    # local host IP '127.0.0.1'

    host = sys.argv[1]
    x = int(ord(host[0]))
    if x > 57:
        host = socket.gethostbyname(host)
    user=str(sys.argv[3])
    # Define the port on which to connect
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))
    s.send(user.encode())
    
    response = str(s.recv(1024).decode())

    if response == "0":
        print("connection failed")
        sys.exit()
    
    f=open("./ClientFiles/Keys/"+user+"Key.txt", "r")
    if f.mode == 'r':
        key=f.read()
    f.close()
    
    d = des()
    ciphered = d.encrypt(key,response,True)

    s.send(ciphered.encode())
    #End oF NONCE

    # message to server
    while True:
        message = input("Your Message? ")
        # encrypt the message 
        ciphered = d.encrypt(key,message,True)
        # message sent to server
        s.send(ciphered.encode())

        # messaga received from server
        data = s.recv(1024)

        # print the received Condition
        print('Condition :', str(data.decode()))

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break
    # close the connection
    s.close()

if __name__ == '__main__':
    Main()
