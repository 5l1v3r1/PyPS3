'''
Patching a lot of addresses at the same time
'''

from pyps3.lib import API
from pyps3.memory import Memory

ip = input('IP: ') # get PS3 address
if API().connect(ip):
    print('Connected!')

    proc = API().getProcs() # get game process
    Memory().memWriteMultiple(
        proc, 
        [
            # teleports us to the juggernog location
            ('0x1780f50', '0x44, 0x77, 110, 0x81, 0xc4, 0xb1, 0xb0, 0x62, 0x43, 0, 0x20'),
            ('0x1786758', '0x44, 0x77, 110, 0x81, 0xc4, 0xb1, 0xb0, 0x62, 0x43, 0, 0x20'), 
            ('0x178bf60', '0x44, 0x77, 110, 0x81, 0xc4, 0xb1, 0xb0, 0x62, 0x43, 0, 0x20'),
            ('0x1791768', '0x44, 0x77, 110, 0x81, 0xc4, 0xb1, 0xb0, 0x62, 0x43, 0, 0x20'),

            # gives us the worst gun of Bo2 zombies, the grenade launcher
            ('0x178118F', '0x41')
        ]
    )