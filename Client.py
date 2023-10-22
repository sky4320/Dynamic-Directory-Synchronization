#CLIENT END CODE
# Name: SIVA KESHAV YALAMANDALA ID: 1001963510

import sys
import socket                                  #importing Socket Library.
import pickle
client_skt = socket.socket()                   #creating client socket
port = 4320                                    #Assiging a port number to connect with server A
arguments = sys.argv
if(len(arguments)>1):
    client_skt.connect(('127.0.0.1', port))        #Here client sends a request to Server A .   
    client_skt.send(pickle.dumps(arguments))
    status = client_skt.recv(3072)
    print(status)

else:
    client_skt.connect(('127.0.0.1', port))
    client_skt.send(pickle.dumps([]))
#retrieving data after sending the request to the server.
    receiveddata=(client_skt.recv(3072).decode())

#Sorting the data.
    Data = receiveddata.split("\n")
    Data.sort(key=str.lower)
    i=0
    print("Filename\tSize\tTime")


#Printing the data after retrieving from the servers.
    while(i < len(Data)):
        if(Data[i] != ''):
            print(Data[i])
        i = i+1                             #Traversing the data by incrementing the i value by 1 each time.

#closing the client side after receiving data from the server. 
#client_skt.close()   
