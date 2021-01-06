# TCP-File-Transfer-Server-Client
A TCP based file transfer server and client

This program does not support Windows as the multiprocessing part is done by os.fork(), please change that part to fit your needs if necessary.

To run the programs, simply type:

python3 server.py YOUR_IP YOUR_PORT 
python3 client.py YOUR_IP YOUR_PORT

for example, I will use

python3 server.py 192.168.0.XXX 8888

for testing

There are four command you can use from client end:

1. list -- retrieve all the files that are currently on the server

2. get file. -- retrive a file from server if exist
   usage:  **get path_or_file_name**

3. put file -- upload a file to the server
   usage:  **put path_or_file_name**

4. quit

more functions will be included in the future
