# ************************************************************ #
#       Library created by Nexus, on 22 August 2021.           #
# ************************************************************ #
# This program is free software: you can redistribute it and/or#
# modify it under the terms of the GNU General Public License  #
# as published by the Free Software Foundation, either version #
# 3 of the License, or (at your option) any later version.     #
#                                                              #
# This program is distributed in the hope that it will be      #
# usefull , but WITHOUT ANY WARRANTY; without even the implied #
# warrantyof MERCHANTABILITY or FITNESS FOR A PARTICULAR       #
# PURPOSE. See the GNU General Public License for more details.#
#                                                              #
# You should have received a copy of the GNU General Public    #
# License along with this program. If not, see                 #
# http://www.gnu.org/licenses/.                                #
#                                                              #
# (C) 2021-2022 PyPS3 by Nexus                                 #
# (C) 2010-2022 multiMAN/webMAN/sMAN/sLaunch/prepNTFS by DeanK #
#                                                              #
# THE SOFTWARE IS DISTRIBUTED "AS IS". NO WARRANTY OF ANY KIND #
# IS EXPRESSED OR IMPLIED. YOU USE AT YOUR OWN RISK. NEITHER   #
# THE AUTHOR, THE LICENSOR NOR THE AGENTS OF THE LICENSOR WILL #
# BE LIABLE FOR DATA LOSS, DAMAGES, LOSS OF PROFITS OR ANY     #
# OTHER KIND OF LOSS WHILE USING OR MISUSING THIS SOFTWARE OR  #
# ITS COMPONENTS. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT   #
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY  #
# , WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,       #
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR   #
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.                   #
# ************************************************************ #

import requests, re, socket, time
from bs4 import BeautifulSoup, ResultSet

from src.exceptions import *
from src.core import Core

class API():
    def __init__(self):
        pass

    def get(self, url):
        req = requests.get(url)
        if req.status_code == 200: return True
        else: raise InvalidHTTPResponse( f'Got status code {str(req.status_code)} as response, which means "{self.HTTP_RESPONSE_CODES[req.status_code]}".')

    def connect(self, ps3ip=None) -> bool: # check if its up
        '''
        Connecs to the PS3

        :param ps3ip str: The Console IP address to connect to
        :return bool: True, False
        '''

        if ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        else:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)

                sock_connect = sock.connect_ex((ps3ip, 80))
                time.sleep(0.2)
                sock.close()

                if sock_connect == 0: # we are able to connect
                    Core.ps3ip = ps3ip
                    return True

            except Exception:
                raise ConsoleConnectionError('Failed to connec to the PS3')
    
    def reboot(self, rbt_type='hard') -> bool:
        '''
        Reboots the PS3

        :param rbt_type str: Reboot type (soft, hard, quick, vsh)
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        if not rbt_type.lower() in ['soft', 'hard', 'quick', 'vsh']: raise InvalidRebootType('Reboot type is invalid')
        else:
            try:
                return self.get(f'http://{Core.ps3ip}/reboot.ps3?{type}')
            except Exception:
                raise RebootException('Failed to reboot')
    
    def shutdown(self) -> bool:
        '''
        Shuts the PS3 down

        :return bool: True, False
        '''
        if Core.ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        else:
            try:
                return self.get(f'http://{Core.ps3ip}/shutdown.ps3')
            except Exception:
                raise ShutdownException('Failed to shit down')
    
    def setled(self, led_clr=None, led_mode=None) -> bool:
        '''
        Change the PS3 LED lights
        
        :param led_clr int: The color (red=0, green=1, yellow=2)
        :param led_mode int: The LED mode (off=0, on=1, blink fast=2, blink slow=3)
        :return bool: True, False
        '''
        if Core.ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        elif led_clr == None or not led_clr in [0, 1, 2]: raise InvalidLedCode('Invalid LED code') 
        elif led_mode == None or not led_mode in [0, 1, 2, 3, 4, 5, 6]: raise InvalidLedMode('Invalid LED mode')
        else:
            try:
                # Red = 0
                # Green = 1
                # Yellow = 2

                # Off = 0
                # On  = 1
                # Blink Fast = 2
                # Blink Slow = 3
                # Blink Alt1 = 4
                # Blink Alt2 = 5
                # Blink Alt3 = 6
                
                return self.get(f'http://{Core.ps3ip}/led.ps3mapi?color={str(led_clr)}&mode={str(led_mode)}')
            except Exception:
                return False
    
    def buzz(self, buzz_mode=1) -> bool:
        '''
        Haha PS3 go buzz buzz, this function makes the Playstation buzzer go off

        :param buzz_mode int: The buzz mode (once=1, twice=2, triple=3)
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        elif buzz_mode == None or not buzz_mode in [1, 2,3]: raise InvalidBuzzMode('Invalid buzz mode') 
        
        else:
            try:
                # once = 1
                # twice = 2
                # triple = 3

                return self.get(f'http://{Core.ps3ip}/buzzer.ps3mapi?mode={str(buzz_mode)}') # buzz endpoint
            except Exception:
                return False

    def getConsoleInfo(self) -> ResultSet: # get the console info
        '''
        Gets the PS3 information, and returns it in a JSON object
        
        :return dict: The JSON object holding all the data'''
        if Core.ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        else:
            try:
                req = self.get(f'http://{Core.ps3ip}/cpursx.ps3?/sman.ps3')

                if req:
                    soup = BeautifulSoup(req.text.encode('utf-8'), 'html.parser')
                    return soup.findAll('a', attrs={'class': 's'})

                else:
                    raise InvalidHTTPResponse( f'Got status code {str(req.status_code)} as response, which means "{self.HTTP_RESPONSE_CODES[req.status_code]}".')

            except Exception:
                return False
    
    def getFirmware(self) -> str:
        '''
        Parses the firmware from the page

        :return str: Returns the console firmware
        '''

        div = self.getconsoleinfo()[0]

        if div == None: raise DivIsNone('Div is none!')
        else:
            try:
                clutter = div[4].text
                firmware = ''

                for l in clutter: 
                    if l != "P": firmware += l
                    else: break
                
                if firmware == None: raise EmptyFirmwareResponse('Console returned empty firmware.')
                else: return firmware.split(': ', 1)[1]
            
            except Exception:
                raise GetFirmwareException('Unable to parse firmware')
    
    def getTemps(self) -> dict:
        '''
        Gets the consoles temperature

        :return dict: Returns the CPU, RSX and max temperature
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('please enter a valid Playstation target IP')
        else:
            page = requests.get(f'http://{Core.ps3ip}/cpursx.ps3?/sman.ps3').text
            cpu, maxtemp, rsx = re.findall(r'<a class=\"s\" href=\"/cpursx.ps3\?up\">CPU: (.*?)\°C \(MAX: (.*?)\°C\)<br>RSX: (.*?)\°C</a>', page)[0]

            return {'cpu': cpu, 'rsx': rsx, 'max': maxtemp}
    
    def setFanSpeed(self, speed: None) -> bool:
        '''
        Sets the fan speed (in %)

        :param speed int: The fan speed (in %)
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('please enter a valid Playstation target IP')
        elif speed == None or not str(speed).isdigit(): raise SpeedIsNone('Speed has to be integer!')
        else:
            return self.get(f'http://{Core.ps3ip}/cpursx.ps3?/sman.ps3?/cpursx.ps3?fan={str(speed)}')
    
    def ejectCD(self) -> bool:
        '''
        Ejects the CD out of the tray

        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('please enter a valid Playstation target IP')
        else:
            return self.get(f'http://{Core.ps3ip}/eject.ps3')
    
    def exitToXMB(self):
        '''
        Exits the game to the XMB screen

        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('please enter a valid Playstation target IP')
        else:
            return self.get(f'http://{Core.ps3ip}/xmb.ps3$exit')
    
    def reloadPS3Game(self):
        '''
        Exits, and re-enters the game

        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('please enter a valid Playstation target IP')
        else:
            return self.get(f'http://{Core.ps3ip}/xmb.ps3$reloadgame')

    def getGameName(self) -> str:
        '''
        Gets the current game name (XMB Menu if no game is being played)

        :return str: Returns the game name
        '''
    
        if Core.ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        else:
            try:
                req = requests.get(f'http://{Core.ps3ip}/cpursx.ps3?/sman.ps3')

                if req.status_code == 200:

                    soup = BeautifulSoup(req.text, 'html.parser')
                    res = soup.findAll('h2')[0].text
                    game = None

                    if res.startswith('BL') or res.startswith('NP') or res.startswith('BC'): game = res.split(' ', 1)[1].encode('ascii', 'ignore').decode()
                    else: game = 'XMB Menu'
                    
                    return game
                else: raise InvalidHTTPResponse( f'Got status code {str(req.status_code)} as response, which means "{self.HTTP_RESPONSE_CODES[req.status_code]}".')
            except Exception:
                raise GetCurrentGameException('Unable to parse game')

    def getProclist(self) -> list:
        '''
        Gets the running processes on the console, use `getProcs()` to get the parsed list
        
        :return list: Returns the running processes
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        else:
            try:
                req = requests.get(f'http://{Core.ps3ip}/home.ps3mapi/sman.ps3')
                if req.status_code == 200:

                    return re.findall('\<select name="proc">(.*?)\</select>', req.text)
                else: raise InvalidHTTPResponse( f'Got status code {str(req.status_code)} as response, which means "{self.HTTP_RESPONSE_CODES[req.status_code]}".')
            
            except Exception:
                raise GetProcListException('Failed to parse process list')
    
    def getProcs(self, gameonly=True) -> dict:
        '''
        Gets the current game(s)
        
        :param gameonly bool: Wether we want the full list, or just the game
        :return dict: Returns the running games in a dict
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        else:
            try:
                procs = self.getproclist(Core.ps3ip)
                procs_list = {}

                for proc in re.findall('\<option value="(.*?)\</option>', procs[1][0]):

                    pid, proc_name = proc.split('"/>')

                    if proc_name.startswith('01000300') or proc_name.startswith('01000400'): pass # if its a system process, skip
                    else: procs_list.update({pid: proc_name})
                
                if len(procs_list) <= 0:
                    return 'No processes found.'

                return procs_list if not gameonly else list(procs_list[1])[0]
            except Exception:
                raise GetProcsException('Failed to parse games')

    def memWrite(self, process=None, patch_addr=None, hex_value=None) -> bool:
        '''
        Patches a specific address with a hex value
        
        :param process str: The process to write it to
        :param patch_addr str/list: The patch address (or addresses)
        :param hex_value str: The new hex value to patch
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        elif process == None: raise ProcessIsNone('Process can\'t be none!')
        elif patch_addr == None: raise PatchAddressIsNone('Patch address can\'t be none!')
        elif hex_value == None: raise HexValueIsNone('Hex value can\'t be none!')
        else:
            patch_addr = patch_addr.replace('0x','').replace('0X','')
            try:

                if type(patch_addr) == list:
                    for addr in patch_addr:
                        req = requests.get(f'http://{Core.ps3ip}/setmem.ps3mapi?proc={process}&addr={addr}&val={hex_value}')
                        if req.status_code == 200: continue
                        else: raise InvalidHTTPResponse( f'Got status code {str(req.status_code)} as response, which means "{self.HTTP_RESPONSE_CODES[req.status_code]}".')
                    return True
                else:
                    return self.get(f'http://{Core.ps3ip}/setmem.ps3mapi?proc={process}&addr={patch_addr}&val={hex_value}')

            except Exception:
                raise MemWriteException('Failed to write to console memory')
    
    def memView(self, process=None, read_addr=None, pretty=False) -> str | list:
        '''
        Reads from the process
        
        :param process str: The process to read from
        :param read_addr str: The patch address to read from
        :return str/list: string if `pretty` has been set to True else list
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        elif process == None: raise ProcessIsNone('Process can\'t be none!')
        elif read_addr == None: raise ReadAddressIsNone('Read address can\'t be none!')
        else:
            try:
                read_addr = read_addr.replace('0x','').replace('0X','')
                process = f'0x{process}' if not process.startswith('0x') else process

                page = requests.get(f'http://{Core.ps3ip}/getmem.ps3mapi?proc={process}&addr={read_addr}&len=256')
                memview = re.findall(r'\<font color=\#ff0\>\<\/font\>\<hr\>(.*?)\<textarea id=\"output\"', page.text)[0]

                return memview.split('<br>') if not pretty \
                    else '\n'.join(memview.split('<br>'))

            except Exception:
                raise MemReadException('Failed to read from console memory')

    
    def memRead(self, process=None, read_addr=None) -> str:
        '''
        Reads from a specific address
        
        :param process str: The process to read from
        :param read_addr str: The patch address to read from
        :return str: memory value
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        elif process == None: raise ProcessIsNone('Process can\'t be none!')
        elif read_addr == None: raise ReadAddressIsNone('Read address can\'t be none!')
        else:
            try:
                read_addr = read_addr.replace('0x','').replace('0X','')
                process = f'0x{process}' if not process.startswith('0x') else process
                
                page = requests.get(f'http://{Core.ps3ip}/getmem.ps3mapi?proc={process}&addr={read_addr}&len=256')
                memview = re.findall(r'\<textarea id=\"output\" style=\"display\:none\"\>(.*?)\<\/textarea\>', page.text)
                return memview[0]

            except Exception:
                raise MemReadException('Failed to read from console memory')
