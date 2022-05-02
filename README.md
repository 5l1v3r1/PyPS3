# **NOTE!**
This library is very unfinished, so very unstable! If you want to use a stable library, just wait for a while!

# PyPS3 PRE-ALPHA!
Python PS3 library to write to the PS3's memory, and more

# Requirements
```
1. All depencies installed (pip install -r requirements.txt)
2. WebMAN installed on the PS3!!!! (Download it from here; https://github.com/aldostools/webMAN-MOD/releases)
```

# Usage
## All examples are for Bo2 zombies, tested on a 4.84 DEX PS3

### Writing to a single address with a single byte
```py
import lib

ip = input('IP: ') # get PS3 address
if lib.API().connect(ip):
    print('Connected!')

    # write to PS3
    lib.API().memwrite(ip, proc, '1780F43', '05') # enable godmode
```

----

### Writing to multiple addresses with a multiple bytes
```py
import lib

ip = input('IP: ') # get PS3 address
if lib.API().connect(ip):
    print('Connected!')

    proc = lib.API().getProcs(ip) # get game process

    # write to PS3
    lib.API().memWrite(proc, '1780F43', '05') # enable godmode
    lib.API().memWrite(proc, '1CB7BF8', '3E80') # enable slowmotion mode
    lib.API().memWrite(proc, '1CAF9D8', '4148') # enable low gravity
```

----

### Setting a single hex value for multiple addresses for a single mod
```py
import lib

ip = input('IP: ') # get PS3 address
if lib.API().connect(ip):
    print('Connected!')

    proc = lib.API().getProcs(ip) # get game process
    lib.API().memWrite(ip, proc, ['1CAF0D8', '1CAF138', '1CAF198'], '49FFFF') # write to the memory
```

----

### Basic Bo2 zombies RTM tool
```py
import lib

class Mods:
    def __init__(self):
        self.OFFSET_ZM_GODMODE = '1780F43'
    
    def dogodmode(self, enable, proc):
        if enable:
            if lib.API().memWrite(proc, self.OFFSET_ZM_GODMODE, '05'): print('Godmode enabled')
        
        elif not enable:
            if lib.API().memWrite(proc, self.OFFSET_ZM_GODMODE, '04'): print('Godmode disabled')

ip = input('IP: ')
if lib.API().connect(ip):
    print('Connected!')

    proc = lib.API().getProcs(ip)

    while 1:
        mod = input('Enter mod: ')
        mod_args = mod.split(' ')

        if mod_args[0] == 'godmode':
            if mod_args[1] == 'enable':
                Mods().dogodmode(True, proc)

            elif mod_args[1] == 'disable':
                Mods().dogodmode(False, proc)
```

# Credits
- [Nexus](https://github.com/Nexuzzzz), for creating the library
- [AldosTools](https://github.com/aldostools), for creating WebMAN (credits to DeanK for creating the original WebMAN)
- [Vivitchka](https://github.com/inthecatsdreams), for some functions and the idea to use WebMAN 
- [GeoHotz](https://github.com/geohot), for pwning the PS3 lol