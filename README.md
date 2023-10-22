# Dynamic-Directory-Synchronization

**DESCRIPTION**

This project involves building a client-server application to synchronize directories across multiple servers, in real-time. It was developed as a part of a course (mention the course name and code, if applicable). The client process connects to two server processes, Server A and Server B, and maintains synchronized directory listings. The project allows for file locking, dynamic updates, and real-time notifications.

This README provides detailed instructions on how to set up and execute the project. The project is open for collaboration, and we welcome contributions and improvements.

**Execution Steps**  
Follow these steps to execute the project:

  Make sure to create Server A and Server B folders in your local.
**Run ServerB.py:**

1. Open a terminal.  
2. Navigate to the project directory.  
3. Execute python ServerB.py to start Server B.  
4. This server represents directory B.  

**Run ServerA.py:**  

1. Open a new terminal.
2. Navigate to the project directory.
3. Execute python ServerA.py to start Server A.
4. This server represents directory A.



**Run the Client.py:**

1. Open another terminal.
2. Navigate to the project directory.
3. Execute python Client.py.
4. The client will connect to Server A.

**Fetching Data:**

- The client sends a request to Server A.
- Server A generates a listing of the contents of directory A.
- Server A connects to Server B.
- Server B generates a listing of the contents of directory B and returns it to Server A.
- Server A combines the listings and sorts them by file name.
- The client receives the composite list, which includes file name, size, and timestamp.
- The client prints the data to the command line.
    

**Real-time Synchronization:**

+ Servers A and B autonomously synchronize directory contents, including file additions, deletions, and modifications.
+ These changes are made in real time.
+ The user is notified of server actions, including which file is being synchronized when applicable.
   
**File Locking:**

* The client provides the option to lock files on Server A by using ./lab3 -lock -index.
* Modifications to locked files in directory B are placed in a separate directory while the file is locked at Server A.
* Server A has a FIFO queue for applying updates to locked files.
      
**Continuous Updates:**
  
If files are added, modified, or deleted in Server A or B, the client must be executed again to retrieve the latest details.
  
**Note: Be sure to change the directory paths in the code to match your specific environment.**

**Collaboration**     
- We would like to encourage collaboration on this project. Please feel free to contribute if you have ideas for improvements, feature enhancements, or bug fixes. Follow these steps to collaborate:

- Fork the repository.

- Make your changes and improvements.

- Submit a pull request with a clear description of your changes.

- Collaborate with other contributors to refine and enhance the project.

**License**  
This project is under the MIT License.

Author  
Siva Keshav Yalamandala  
Contact Information - sxy3510@mavs.uta.edu
