'''
Basic Bo2 zombies RTM tool
'''

from pyps3.lib import API
from pyps3.memory import Memory

class Mods:
    def __init__(self):
        self.OFFSET_ZM_GODMODE = '1780F43'
    
    def dogodmode(self, enable, proc):
        if enable:
            if Memory().memWrite(proc, self.OFFSET_ZM_GODMODE, '05'): print('Godmode enabled')
        elif not enable:
            if Memory().memWrite(proc, self.OFFSET_ZM_GODMODE, '04'): print('Godmode disabled')

ip = input('IP: ')

if API().connect(ip):
    print('Connected!')

    proc = API().getProcs()

    while 1:
        mod = input('Enter mod: ')
        mod_args = mod.split(' ')

        if mod_args[0] == 'godmode':
            if mod_args[1] == 'enable':
                Mods().dogodmode(True, proc)

            elif mod_args[1] == 'disable':
                Mods().dogodmode(False, proc)