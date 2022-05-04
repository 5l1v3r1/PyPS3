'''
Setting a single hex value for multiple addresses for a single mod
'''

from pyps3.lib import API
from pyps3.memory import Memory

ip = input('IP: ') # get PS3 address
if API().connect(ip):
    print('Connected!')

    proc = API().getProcs() # get game process
    Memory().memWrite(proc, ['1CAF0D8', '1CAF138', '1CAF198'], '49FFFF') # write to the memory