#!/usr/bin/python
import paramiko

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('169.254.204.32', username='test',password='root123')

# Get the List of files
#stdin, stdout, stderr = ssh.exec_command("ls -l /")
#print stdout.read()

# Get the ipTables information
stdin, stdout, stderr = ssh.exec_command("sudo -S dmidecode -t 1")
stdin.write('root123\n')
stdin.flush()
print stdout.read()



