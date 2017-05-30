#!/usr/bin/python
import paramiko
import sys
import time
import select

'''
  run the Program using python class_paramiko.py "command"

'''

class SSHClient:
   
    TIMER_THRESHOLD =15

    def __init__(self, serverIP, user, Passwd):
        self.serverIPAddress = serverIP
        self.userName = user
        self.password = Passwd
        self.client_connection= None
        self.reconnect_time = 1


    # Establish the connection
    def make_connection(self):

        while True:
            try:
                self.client_connection = paramiko.SSHClient()
                self.client_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.client_connection.connect(self.serverIPAddress, username=self.userName, password=self.password)
                print "connection is Established"
                break;

            except paramiko.AuthenticationException:
                print "Authentication failed when connecting to %s" % self.serverIPAddress
                print "Change the serverIP address, userName and Password"
                sys.exit(1)

            except:
                print "Could not SSH to %s, waiting for it to start" % self.serverIPAddress
                self.reconnect_time += 1
                time.sleep(1)

                # If we could not connect within time limit
                if (self.reconnect_time  == SSHClient.TIMER_THRESHOLD):
                    print "Could not connect to %s. Giving up" % self.serverIPAddress
                    sys.exit(1)
                  
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


            # Another way of printing the data using SELECT CALL
            # Wait for the command to terminate
            while not stdout.channel.exit_status_ready():
               # Only print data if there is data to read in the channel
               if stdout.channel.recv_ready():
                 rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                
                 if len(rl) > 0:
                    # Print data from stdout
                    print stdout.channel.recv(1024)
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
    

