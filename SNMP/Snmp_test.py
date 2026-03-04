import asyncio
from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    UsmUserData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
    usmHMACSHAAuthProtocol,
    usmAesCfb128Protocol
)

IP = '192.168.58.102'
USER = 'admin'
AUTH_KEY = 'Huawei@123'
PRIV_KEY = 'Huawei@123'

async def snmp_get():
    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
        SnmpEngine(),
        UsmUserData(
            userName=USER,
            authKey=AUTH_KEY,
            privKey=PRIV_KEY,
            authProtocol=usmHMACSHAAuthProtocol,
            privProtocol=usmAesCfb128Protocol
        ),
        UdpTransportTarget((IP, 161), timeout=2, retries=1),
        ContextData(),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
    )

    if errorIndication:
        print("SNMP Error:", errorIndication)
        return

    if errorStatus:
        print(
            '%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
            )
        )
        return

    for oid, value in varBinds:
        print(f"{oid.prettyPrint()} = {value.prettyPrint()}")

asyncio.run(snmp_get())
