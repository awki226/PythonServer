# PythonServer

## <h1> Abstract: 
  The purpose of this project was to create a client and server program that was a shared folder server that allowed for uploads and downloading files, along with this the client could view the Download/Upload speed of the file. Also the client is able to print out the directory of the files on the server and view the size of file when they were uploaded.

### <h2> Introduction: 
  The shared folder is based wherever the Server.py is located, this allows for the file to be moved to other directories on the machine and still allows for multiple folders to be shared based on the execution path where Server.py is; however, this implementation does not allow the client to change directories only send, request, delete files, along with view the contents of the directory. To run the program the user must compile each .py file with $python3 file.py, Server.py must be running or the client.py cannot connect. The Client.py file has two separate functions Download and Upload that send the request and handle each of it’s functions respectively. To view the speed I used a popular progress bar library from the third party tqdm, which I used a reference from this website here on how to use the tqdm library https://tqdm.github.io/docs/tqdm/. Printing the directory and deleting the file was handled within the conditional
statement. The server handled each of these request sent to it.
  
    HOW TO USE THE Client.py:
    $python Client.py
    $42069
    This is the port number
    Will then ask for function
    Enter in like so into the terminal: 
    UPLOAD
    DOWNLOAD
    PRINT
    DELETE
    
Then you will be prompted to input a filename for three of the functions
     
    Implementation:
    SERVER.py
    
The other request where handled within their respective conditional loops. The Server.py was set up using the serversocket built in library that comes with python 3, I chose this library since I could make TCP handler that would run for quite awhile without timing out. Within this handler I set it to processes requests using conditional if statements, to process requests made by the client. 
### <h3> The Upload branch:
  
  receives bytes from the client and writes them to a file based on information that it received prior being filename, and file size. The Download branch send bytes of the requested file until the end of file byte is read, this branch also determines before the process is ran if the file exists and notifies the user before running. The Delete branch checks to see if the file exists first if it does it removes it from the directory; however, if the file does not exist the client receives a message stating that the file does not exist. The print branch looks through the directory collecting data such as filename, file size, and upload time/date. From here it creates a string and sends it to the client to print on there respected side. Below is how the upload/download are handled on the server side.
I would show the Upload function but it looks the same and my MacBook ran out of physical space on the hard drive to do so as well.

#### <h4> The print function:
  provides the user with the attributes of all the files where the server.py is located and is implemented by branch condition, and was implemented via the os libary. The Delete request sends the filename to be deleted and is responded with the acknowledgement if the file was deleted or not, this was implemented via the os library.
Evaluation:
