import paramiko

ip='10.17.171.175'
port=22
username='root'
password='interOP@123sys'

cmd='ls /opt/nimsoft'

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,port,username,password)

stdin,stdout,stderr=ssh.exec_command(cmd)
outlines=stdout.readlines()
# print(outlines)
resp=''.join(outlines)
print(resp)