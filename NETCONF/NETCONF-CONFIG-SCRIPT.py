import time
import paramiko
from ncclient import manager

# Configuration Constants
DEVICE_PARAMS = {
    "ip": "192.168.58.100",
    "ssh_user": "python",
    "ssh_pass": "Huawei12#$",
    "nc_port": 830,
    "nc_user": "netconf",
    "nc_pass": "Huawei12#$"
}

# XML Template for Interface Configuration
XML_CONFIG = '''<config>
    <ethernet xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <ethernetIfs>
            <ethernetIf operation="merge">
                <ifName>GE1/0/2</ifName>
                <l2Enable>disable</l2Enable>
            </ethernetIf>
        </ethernetIfs>
    </ethernet>
    <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <interfaces>
            <interface operation="merge">
                <ifName>GE1/0/2</ifName>
                <ifDescr>Config by NETCONF</ifDescr>
                <ifmAm4>
                    <am4CfgAddrs>
                        <am4CfgAddr operation="create">
                            <subnetMask>255.255.255.0</subnetMask>
                            <addrType>main</addrType>
                            <ifIpAddr>192.168.2.1</ifIpAddr>
                        </am4CfgAddr>
                    </am4CfgAddrs>
                </ifmAm4>
            </interface>
        </interfaces>
    </ifm>
</config>'''

def enable_netconf_via_ssh():
    """Step 1: Use Paramiko to enable NETCONF services on the device."""
    print(f"Connecting to {DEVICE_PARAMS['ip']} via SSH to enable NETCONF...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(
            hostname=DEVICE_PARAMS['ip'], 
            username=DEVICE_PARAMS['ssh_user'], 
            password=DEVICE_PARAMS['ssh_pass']
        )
        
        with ssh.invoke_shell() as channel:
            commands = [
                "system-view",
                "aaa",
                f"local-user {DEVICE_PARAMS['nc_user']} password irreversible-cipher {DEVICE_PARAMS['nc_pass']}",
                f"local-user {DEVICE_PARAMS['nc_user']} service-type ssh",
                f"local-user {DEVICE_PARAMS['nc_user']} privilege level 3",
                "quit",
                f"ssh user {DEVICE_PARAMS['nc_user']} authentication-type password",
                f"ssh user {DEVICE_PARAMS['nc_user']} service-type snetconf",
                "snetconf server enable",
                "netconf protocol inbound ssh port 830",
                "return"
            ]
            
            for cmd in commands:
                channel.send(cmd + "\n")
                time.sleep(0.5)
            
            output = channel.recv(10000).decode()
            print("SSH Configuration Output:\n", output)
            
    finally:
        ssh.close()

def configure_interface_netconf():
    """Step 2: Use ncclient to send NETCONF XML configuration."""
    print("Connecting via NETCONF...")
    
    try:
        with manager.connect(
            host=DEVICE_PARAMS['ip'],
            port=DEVICE_PARAMS['nc_port'],
            username=DEVICE_PARAMS['nc_user'],
            password=DEVICE_PARAMS['nc_pass'],
            hostkey_verify=False,
            device_params={'name': 'huawei'}, # Critical for Huawei VRP support
            allow_agent=False,
            look_for_keys=False
        ) as m:
            print("NETCONF session established. Sending configuration...")
            response = m.edit_config(target='running', config=XML_CONFIG)
            print("Response from Device:", response)
            
    except Exception as e:
        print(f"NETCONF Error: {e}")

if __name__ == "__main__":
    # 1. First Enable NETCONF on the device
    enable_netconf_via_ssh()
    
    # 2. Then apply interface configs via NETCONF
    time.sleep(2) # Brief pause for service to initialize
    configure_interface_netconf()