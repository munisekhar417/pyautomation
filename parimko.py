#!/usr/bin/python
import paramiko

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('169.254.204.32', username='test',password='root123')
stdin, stdout, stderr = ssh.exec_command("ifconfig -a")
#print stdout.read()
liststr=[]
liststr=stdout.read().splitlines()
print liststr

newlist=[]
for line in liststr:
   line= line.strip()
   newlist.append(line)

print newlist


