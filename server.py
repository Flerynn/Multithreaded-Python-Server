import socket
import threading
import sys
import random
import time
from pydes import des

#Get the UserNames
f=open("./ServerFiles/names.txt", "r")
if f.mode == 'r':
	names=f.read()
	names=names.split('\n')
f.close()

#Random Seeds
random.seed(time.time())

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        print("Server Running...") 
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            print('Connected to :', address[0], ':', address[1])
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        response = str(random.randint(1,100000000000))
        username = client.recv(size).decode()
        if username in names:
            client.send(response.encode())
        else:
            response = str(0)
            client.send(response.encode())
            print('Disconnected :', address[0], ':', address[1])
            client.close()
            return False
        fl=open("./ServerFiles/Keys/"+username+"Key.txt", "r")
        if fl.mode == 'r':
            key=fl.read()
        fl.close()

        Nonce_Res = client.recv(size).decode()
        
        d = des()
        plain = d.decrypt(key,Nonce_Res,True)

        if plain != response:
            client.close()
            print('Disconnected :', address[0], ':', address[1])
            return False
        
        while True:
            try:
                data = client.recv(size).decode()
                # decrypt the messaga
                plain = d.decrypt(key,data,True)
                if plain:
                    # store the message in the logs
                    fs=open("./ServerFiles/Log/"+username+"Log.txt", "a")
                    fs.write(plain + "\n")
                    fs.close()
                    # Successful save ..
                    response = "Successful"
                    client.send(response.encode())
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                print('Disconnected :', address[0], ':', address[1])
                return False

if __name__ == "__main__":
    while True:
        port_num = 12345
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedServer('',port_num).listen()
