import paramiko
import time

ip = "192.168.58.100"
username = "python"
password = "Huawei12#$"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username=username, password=password)

cli = ssh.invoke_shell()
cli.send('n\n')
cli.send('screen-length 0 temporary\n')
cli.send('display cu\n')
time.sleep(3)
dis_cu = cli.recv(999999).decode()
print (dis_cu)
ssh.close
