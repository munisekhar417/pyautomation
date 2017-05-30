#!/usr/bin/python
import paramiko
import sys

'''
  run the Program using python class_paramiko.py "command"

'''
class SSHClient:

    def __init__(self, serverIP, user, Passwd):
        self.serverIPAddress = serverIP
        self.userName = user
        self.password = Passwd
        self.client_connection= None

    # Establish the connection
    def make_connection(self):
        try:
            self.client_connection = paramiko.SSHClient()
            self.client_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client_connection.connect(self.serverIPAddress, username=self.userName, password=self.password)

        except paramiko.AuthenticationException:
            print "Authentication failed when connecting to %s" % self.serverIPAddress
            print "Change the serverIP address, userName and Password"

        finally:
            print "Make Function is done"
        

    def execute_commands(self, command):

        if(command):
            # Execute Command with out SUDO
            #stdin, stdout, stderr = self.client_connection.exec_command(command)
           

            # With Sudo add -S option and Append to the command to be executed
            command = 'sudo -S ' + str(command)
            stdin, stdout, stderr = self.client_connection.exec_command(command)
            # Enter the password for Sudo       
            stdin.write(str(self.password)+'\n')
            stdin.flush()
            print stdout.read()
            
        else:
            print "No Command is to Execute"

    def close_connection(self):
         self.client_connection.close()


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
    
    # Execute Commands
    client.execute_commands(command)

    # Close the connection
    client.close_connection()
    

