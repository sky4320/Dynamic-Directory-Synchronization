#Server A code
# Name: SIVA KESHAV YALAMANDALA ID: 1001963510

import socket                                                 #importing socket library 
import os                                                     #importing os library for file management     
import sys                                                    #importing sys library inorder to use system specific parameters and functions
import time                                                   #importing time library for printing modified time
import pickle                                                 #importing pickle library for serializing and de-serializing a Python object structure
import threading                                              #importing thread package for parallel processing
import shutil                                                 #importing shutil package for copying files between directory
import filecmp                                                #importing filecmp for comparing the files between files 
import dirsync

stat_var = 2
lock_file = ""
uoplist = []
initialfilesinB = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB")
initialfilesinA = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA")
remove = 0
add = 0
#modifiedtimes ={}
#for item in initialfilesinA:
 #   modifiedtimes[item] = os.path.getmtime(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA"+"/"+item)
def connection():                                             #defining fucntion connection to estabilish connection with client and Server A
    global lock_file, uoplist, stat_var
    skt1 = socket.socket()
    
    print('Socket has been estabilished successfully in ServerA')
    #Assigning port numbers
    port1 = 4320
    
    skt1.bind(('', port1))                                    #binding Server A with port
    print('Socket binding successful!!!')
    skt1.listen()
    print('Server A listening')
    dirsync.sync(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA",r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB",'sync',twoway=True, create=True)

    data=connectiontoserverb()

    
    
    #directory read operation and fetching the data and appending it
    while True:
        new_obj, client_ad = skt1.accept()
        print('Got connection from', client_ad)
        dir_path = r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA"
        files = os.listdir(dir_path)                         #lisiting the files retrieved from Server A.
        data_client = b''+ new_obj.recv(3072)
        if(data_client != b''):
            client_arguements = pickle.loads(data_client)
            if(len(client_arguements)>1):
                if(int(client_arguements[2][1]) > len(files) - 1):
                    errormsg = "error message"
                    new_obg.send(errormsg.encode())
                elif(client_arguements[1]=="-lock" and stat_var == 2):
                    stat_var = 0
                    lock_file = files[int(client_arguements[2][1])]
                    new_obj.send("file locking success".encode())
                elif(client_arguements[1]=="-unlock" and stat_var == 0):
                    stat_var = 1
                    new_obj.send("file unlocking success".encode())
                elif(stat_var == 2):
                    new_obj.send("tried unlocking before locking",encode())

        if(stat_var== 1 ):
            for op in uoplist:
                if(op == "remove_file"):
                    os.remove(os.path.join(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA",lock_file))
                elif(op == "modify_file"):
                    os.remove(os.path.join(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA",lock_file))
                    shutil.copy2(os.path.join(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB",lock_file),r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA")
                else:
                    shutil.copy2(os.path.join(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB",lock_file),r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA")

            uoplist=[]
            stat_var=2
            
        
                    
        msg=""
        size= ""
        modifiedtime=""
        i=0
        while( i < len(files)):
            creation=os.path.getctime(dir_path+"/"+files[i])              #Gets file creation time
            size = str(os.path.getsize(dir_path+"/"+files[i]))#Traversing the list till the end.
            if(stat_var == 0):
                if(files[i]==lock_file):
                    modifiedtime = str(time.ctime(creation))                      #Coverting the time to human readable format
                    msg= msg+"\n"+ files[i] + "\t"+ size +"\t"+  str(modifiedtime) + "\t Locked"
                else:
                    modifiedtime = str(time.ctime(creation))                      #Coverting the time to human readable format
                    msg= msg+"\n"+ files[i] + "\t"+ size +"\t"+  str(modifiedtime)
            else:
                modifiedtime = str(time.ctime(creation))                      #Coverting the time to human readable format
                msg= msg+"\n"+ files[i] + "\t"+ size +"\t"+  str(modifiedtime)
            i=i+1                                                         #Incrementing to retrive the next file name present in the list.
       
    
        #connection to serverB
        
                  
        msg.strip(" ")
        if(len(client_arguements) == 0):
            new_obj.send(msg.encode())

    new_obj.close()
    
def connectiontoserverb():
    global lock_file, uoplist, stat_var,initialfilesinA
    
    threading.Timer(5.0, connectiontoserverb).start()       #connectin serverB will be calling itself for every 5 seconds
    skt2 = socket.socket()                                  #Creating  socket 
    port2= 7999                                             #defining the port number inorder to bind with Server B
    skt2.connect(('127.0.0.1', port2))
    fullmsg = b''                                           
    receiveddata = fullmsg + skt2.recv(4098)               #receives data from the server
    remove=0
    add=0
                                                             #print(receiveddata)
    if(receiveddata != b''):                                 #if any data from server b is added it will execute the loop
        lst = pickle.loads(receiveddata)
        flist = lst[0]
        print(lst)
        filesinB = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB")
        filesinA = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA")
       
        if(lst[0] in filesinA):                             #if delete operation happened in directory B will, increament remove
            remove = 1
        elif(lst[0] not in filesinA):
            add = 1
            
        if((len(filesinA) > len(filesinB)) and remove):         #performs delete option in directory A
            if(flist != lock_file):
                os.remove(os.path.join(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA",flist))
            else:
                if "remove_file" not in uoplist:
                    uoplist.append("remove_file")
            
        elif(len(filesinA) < len(filesinB) and add):            #performs delete option in directory B
            if(flist != lock_file):
                shutil.copy2(os.path.join(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB",lst[0]), r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA/")
            else:
                if "add_file" not in uoplist:
                    uoplist.append("add_file")


        else:
            if(flist != lock_file): 
                os.remove(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA/"+lst[0])   #if there is any latest version the file copies to it in both the servers.
                shutil.copy2(os.path.join(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB",lst[0]), r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA/")
            else:
                if "modify_file" not in uoplist:
                    uoplist.append("modify_file")
    #filesinA = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA/")
    
    d = filecmp.dircmp(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB",r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA")
       
    com_var = d.diff_files


    
    if lock_file in com_var:
        com_var.remove(lock_file)
    modifiedfile = 0
    modifiedtimeofB= os.path.getmtime(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB")     #time modification of files in ServerB
    modifiedTimeofA = os.path.getmtime(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA")  #time modification of files in ServerA
    filesinA = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA")                #listing the files of ServerA
    filesinB = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB")                #listing the files of Server B
        
    if((modifiedTimeofA > modifiedtimeofB) or d ):                                                           #comparing any modification in server A
        print("There is no data from serverb")
        filesinB = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB")
        filesinA = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA")


        if((len(filesinA) > len(initialfilesinA)) and (len(filesinA) > len(filesinB))):              #comparing the number of files present in both the servers, if there is any change files will be updated in Server A
            addedfile = [item for item in filesinA if item not in filesinB]
            shutil.copy2(os.path.join(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA",addedfile[0]), r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB/")
            #modifiedtimes[addedfile[0]] = os.path.getmtime(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA" +"/"+addedfile[0])


        elif((len(filesinA) < len(initialfilesinA)) and (len(filesinA) < len(filesinB))):            #comparing the number of files present in both the servers, if there is any change files will be updated in Server B
                deletedfile = [item for item in filesinB if item not in filesinA]
                if lock_file != deletedfile[0]:
                    os.remove(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB/"+deletedfile[0])


                
        elif(len(com_var) and( os.path.getmtime(os.path.join(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB",com_var[0])) < os.path.getmtime(os.path.join(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA",com_var[0])))): #if file get modified in Server A it should be updated in Server B
            os.remove(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB/"+com_var[0])
            shutil.copy2(os.path.join(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA",d.diff_files[0]), r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB/")
                
    initialfilesinA = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA")
    
def main():
    connection()                                            #invoking connection function to estabilish 

if __name__ == "__main__":
    main()

