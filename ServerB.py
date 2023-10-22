#               ServerB code
# Name: SIVA KESHAV YALAMANDALA ID: 1001963510

import socket                                                       #importing socket library 
import os                                                           #importing os library for file management
import sys                                                          #importing sys library inorder to use system specific parameters and functions
import time                                                         #importing time library inorder to use the modified time
import threading                                                     #importing thread package for parallel
import pickle                                                       #importing pickle library for serializing and de-serializing a Python object structure
import filecmp                                                      #importing filecmp for comparing the files between files 
import dirsync
dir_path = r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB"
dirA_path = r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA"
modifiedtime = os.path.getmtime(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB")
#accesstime = os.path.getatime(dir_path)
initialfiles = os.listdir(dir_path)
modifiedfile = 0

modifiedtimes ={}
for item in initialfiles:
    modifiedtimes[item] = os.path.getmtime(dir_path+"/"+item)

new_obj = 0

def connection():                            #making a connection with server A
    sk2= socket.socket()
    port2 = 7999
    sk2.bind(('',port2))
    sk2.listen()
    dirsync.sync(dir_path,dirA_path,'sync', twoway= True, create=True)
    
    while True:
        new_obj, client_ad= sk2.accept()
        
        files = checkdirectory()                    # check directory B periodically
           

        if(files != None):
            new_obj.send(pickle.dumps(files))          #sends the objects to directory A
    new_obj.close()       
def checkdirectory():                                  # checks directory B

    new_list = []
    get_serverB = os.listdir(dir_path)
    Baccesstime = os.path.getmtime(dir_path)
    global modifiedtime
    global initialfiles
    global modifiedfile
    latermodifiedtime = os.path.getmtime(dir_path)
    global modifiedtimes
    modifiedfiles = os.listdir(dir_path)

    d = filecmp.dircmp(dir_path,dirA_path)
    modifiedfile = d.diff_files

    if(modifiedtime != Baccesstime or modifiedfile):              # checks if any modifications are done to directory B
        
        Baccesstime = os.path.getmtime(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerB")
        modifiedfiles = os.listdir(dir_path)
        #print(modifiedfiles)
        #print(initialfiles)
        if(len(initialfiles) > len(modifiedfiles)):                      #if a file got deleted in directory A
            print("Deleting")
            filesinA = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA")
            print(filesinA)
            deletedfile = [item for item in initialfiles if item not in modifiedfiles]
            print(deletedfile)
            if deletedfile[0] in filesinA:
                print("deleting inside")
               # modifiedtimes.pop(deletedfile[0])
                initialfiles = modifiedfiles
                modifiedtime = latermodifiedtime
                print(deletedfile)
                return deletedfile
           # else:
            #    modifiedtime = latermodifiedtime
             #   return None
        elif(len(initialfiles) < len(modifiedfiles)):                      #checks if a file got added into directory B
            filesinA = os.listdir(r"C:\Users\sandh\Desktop\lab2_yalamandala_sxy3510\ServerA")
            addedfile = [item for item in modifiedfiles if item not in initialfiles]
            print("Addedfile",addedfile)
            if addedfile[0] not in filesinA:
                print("inside adding");
                
                initialfiles = modifiedfiles
                modifiedtime = latermodifiedtime
                print("added files")
                return addedfile
            #else:
             #   modifiedtime = latermodifiedtime
              #  return None
        elif(len(modifiedfile)):                                              #checks if any file contents got updated 
            for tempfile in modifiedfile :
                if(os.path.getmtime(os.path.join(dir_path,tempfile))> os.path.getmtime(os.path.join(dirA_path,tempfile))) :
                   intialfiles = modifiedfiles
                   modifiedtime = Baccesstime
                   new_list.append(tempfile)
            return new_list
        new_list = []
            #temp = modifiedfile
            #modifiedtime = latermodifiedtime
            #initialfiles = modifiedfiles
            #print("files modified")
            
            #return modifiedfile
    #for item in initialfiles:
     #   modifiedtimes[item] = os.path.getmtime(dir_path+"/"+item)
    
def main():
    t1= threading.Thread(target=connection)
    t1.start()
    t1.join()
    
if __name__ == "__main__":
    main()
