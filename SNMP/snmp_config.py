import paramiko
import time
from pysnmp.hlapi import Udp6TransportTarget, SnmpEngine, UsmUserData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd
from pysnmp.hlapi.auth import usmHMACSHAAuthProtocol, usmAesCfb128Protocol 

# Switch Info
ip = '192.168.58.102'
username='python'
password='Huawei@123'

# SSH login
ssh = paramiko.client.SSHClient()
ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
ssh.connect(hostname=ip,port=22,username=username,password=password)
print(ip+' login succesfully')

# Open a channel and enter the configuration.
cli = ssh.invoke_shell()
cli.send('N\n')
time.sleep(0.5)
cli.send('screen-length 0 temporary\n')
time.sleep(0.5)
# Run the following command to go to the system view:
cli.send('system-view immediately\n')
time.sleep(0.5)

# Read the snmp.txt file in the same local folder line by line and write the file to the SSH channel.
f = open('snmp.txt','r')
snmp_config_list = f.readlines()
for i in snmp_config_list:
    cli.send(i)
    time.sleep(0.5)

# Set up an SNMP channel.

g = getCmd(SnmpEngine(),
    UdpTransportTarget((ip,161)),
    UsmUserData('admin','Huawei@123','Huawei@123',authProtocol=usmHMACSHAAuthProtocol,privProtocol=usmAesCfb128Protocol),
    ContextData(),
    ObjectType(ObjectIdentity('SNMPv2-MIB','sysName',0)))
errorIndication, errorStatus, errorIndex, varBinds =next(g)
for i in varBinds:
    print (i)
    print (str(i).split('=')[1].strip())

dis_this = cli.recv(999999).decode() # View the script interaction process.
print (dis_this)
# Close the session.
ssh.close()