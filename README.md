# **NOTE!**
This library is very unfinished, so very unstable! If you want to use a stable library, just wait for a while!

# PyPS3 PRE-ALPHA!
Python PS3 library to write to the PS3's memory, and more

# Requirements
```
1. Requests (pip3 install requests)
2. Beautiful Soup4 (pip3 install bs4)
3. WebMAN installed on the PS3!!!! (IMPORTANT)
```
# Usage
### All examples are for Bo2 zombies

Writing to a single address with a single byte
```py
import lib

ip = input('IP: ') # get PS3 address
proc = list(lib.API().getprocs(ip)[1])[0] # get game process

# write to PS3
lib.API().memwrite(ip, proc, '1780F43', '05') # enable godmode
```
----

Writing to multiple addresses with a multiple bytes
```py
import lib

ip = input('IP: ') # get PS3 address
proc = list(lib.API().getprocs(ip)[1])[0] # get game process

# write to PS3
lib.API().memwrite(ip, proc, '1780F43', '05') # enable godmode
lib.API().memwrite(ip, proc, '1CB7BF8', '3E 80') # enable slowmotion mode
lib.API().memwrite(ip, proc, '1CAF9D8', '41 48') # enable low gravity
```
----

Writing to multiple addresses for a single mod
```py
import lib

ip = input('IP: ') # get PS3 address
proc = list(lib.API().getprocs(ip)[1])[0] # get game process

# write to PS3
for addr in ['1CAF0D8', '1CAF138', '1CAF198']: # this is to enable the far knife mod
    lib.API().memwrite(ip, proc, addr, '49 FF FF') # write to the memory
```
----

Basic Bo2 zombies RTM tool
```py
import lib

class Mods:
	def __init__(self):
		self.OFFSET_ZM_GODMODE = '1780F43'
	
	def dogodmode(self, enable, ip, proc):
		if enable:
			if lib.API().memwrite(ip, proc, self.OFFSET_ZM_GODMODE, '05'): print('Godmode enabled')
		
		elif not enable:
			if lib.API().memwrite(ip, proc, self.OFFSET_ZM_GODMODE, '04'): print('Godmode disabled')

ip = input('IP: ')
proc = list(lib.API().getprocs(ip)[1])[0]

while 1:
	mod = input('Enter mod: ')
	mod_args = mod.split(' ')

	if mod_args[0] == 'godmode':
		if mod_args[1] == 'enable':
			Mods().dogodmode(True, ip, proc)
		elif mod_args[1] == 'disable':
			Mods().dogodmode(False, ip, proc)
```

# Credits
- Nexus, for creating the library
- AldosTools, for creating WebMAN
- Vivitchka, for some functions and the idea to use WebMAN 
- GeoHotz, for pwning the PS3 lol
