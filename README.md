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
Example usage:
```
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
