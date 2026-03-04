
import paramiko 
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname = '192.168.58.100', username = 'python', key_filename= r'C:\Users\PC\.ssh\id_rsa')
cli = ssh.invoke_shell()
cli.send('screen-length 0 temporary\n')
cli.send('display cu\n')
time.sleep(3)
dis_cu = cli.recv(999999).decode()
print (dis_cu)
ssh.close
 