'''
Writing to a single address with a single byte
'''

from pyps3.lib import API
from pyps3.memory import Memory

ip = input('IP: ') # get PS3 address
if API().connect(ip):
    print('Connected!')

    proc = API().getProcs()

    # write to PS3
    Memory().memwrite(ip, proc, '1780F43', '05') # enable godmode