#!/usr/bin/python
import paramiko
import sys
import threading
import time

'''
  run the Program using python class_paramiko.py "command"

'''
class SSHClient:

    def __init__(self, serverIP, user, Passwd):
        self.serverIPAddress = serverIP
        self.userName = user
        self.password = Passwd

        self.client_connection= None
        self.shell= None
        self.transport = None


    # Establish the connection
    def make_connection(self):
        try:
            self.client_connection = paramiko.SSHClient()
            self.client_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client_connection.connect(self.serverIPAddress, username=self.userName, password=self.password)

            # By Using paramiko.SSHClient() you will not get output until executed command exits.
            # If you want to read the output simultaniously when the executing command it throws output ?
            # Use  paramiko.Transport() method
            self.transport = paramiko.Transport(self.serverIPAddress, 22)
            self.transport.connect(username=self.userName, password=self.password)

            # Create the thread and assign the function (process) to start in this thread.
            # thread = threading.Thread(target = self.receive_process)
            #thread.daemon = True
            # thread.start()


        except paramiko.AuthenticationException:
            print "Authentication failed when connecting to %s" % self.serverIPAddress
            print "Change the serverIP address, userName and Password"
         
        except:
            print "Unknown error"
            quit()

        finally:
            print "Make Function is done"

    ''' Open Interactive shell using invoke_shell
    '''
    def open_interactive_shell(self):

        self.shell= self.client_connection.invoke_shell()


    '''Send the commands in to the shell
    '''
    def send_commands_into_shell(self, command):
        if(command):
            if(self.shell):
                self.shell.send(command + "\n")
            else:
                print "shell is not opened"
            
        else:
            print "No Command is to Execute"

    ''' Recieve the Data in the seperate thread
    '''
    def receive_process(self):
        alldata=""
        while(self.shell != None and self.shell.recv_ready()):
            alldata += self.shell.recv(1024)
        print alldata


    '''
       Flush the recv Buffer
    '''
    def flush_recv_buffer(self, wait_time, should_print):
        
        # Wait a bit, if necessary
        time.sleep(wait_time)

        # Flush the receive buffer
        receive_buffer = self.shell.recv(1024)

        # Print the receive buffer, if necessary
        if should_print:
            print receive_buffer
    
      
    ''' Close Connection
    '''
    def close_connection(self):
        if(self.client_connection != None):
            self.client_connection.close()
            self.transport.close()
               

if __name__ == '__main__':

    serverIP = "169.254.204.32"
    user     = "test"
    passwd   = "root123"

    print "HELP :: provide the command to execute, For example ifconfig -a, Otherwise you will end up with error"

    # Intialise the object
    client = SSHClient(serverIP, user, passwd)

    # Establish the connection
    client.make_connection()
  
    command = None
    # Take the command from console
    command = sys.argv[1]
    
    # Open the Shell
    client.open_interactive_shell()

    # Wait for the command to complete
    client.send_commands_into_shell("su")

    # Flush the recv buffer , you can set to False for not printing
    client.flush_recv_buffer(1, True)

    # Wait for the command to complete
    client.send_commands_into_shell(passwd)
   
    # Flush the recv buffer
    client.flush_recv_buffer(1, True)

    # Wait for the command to complete
    client.send_commands_into_shell(command)


    time.sleep(1)
    client.receive_process()


    # Close the connection
    client.close_connection()
    

