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
# warrant yof MERCHANTABILITY or FITNESS FOR A PARTICULAR      #
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

from pyps3.src.exceptions import *
from pyps3.src.core import Core

class API():
    def __init__(self):
        pass

    def get(self, url) -> bool | InvalidHTTPResponse:
        '''
        Helper function to request a page, and return True if it succeeded
        
        :param str url: The URL to request
        :return bool: Returns True if it succeeded, or throws an error if it failed
        '''

        req = requests.get(url) 
        if req.status_code == 200: return True
        else: raise InvalidHTTPResponse( f'Got status code {str(req.status_code)} as response, which means "{self.HTTP_RESPONSE_CODES[req.status_code]}".')
    
    def clean(self, input_) -> str:
        '''
        Helper function to clean a address or hex value
        
        :param input_ str:
        :return str: Returns the cleaned object
        '''

        output = ''.join(input_) if type(input_) == list else input_ # allows lists
        for old, new in [
                (',', ''), # removes commas
                (' ', ''), # removes spaces
                ('0x', ''), # removes this, used by C# CCAPI and stuff as bytes
                ('0X', ''), # same as above, but uppercase
            ]:
            output=output.replace(old, new)
        
        return output

    def connect(self, ps3ip=None) -> bool: # check if its up
        '''
        Connecs to the PS3

        :param ps3ip str: The Console IP address to connect to
        :return bool: True, False
        '''

        if ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        else:
            try:
                

                if self.get(f'http://{ps3ip}/index.ps3'):
                    Core.ps3ip = ps3ip
                    return True

            except Exception:
                raise ConsoleConnectionError('Failed to connect to the PS3')
    
    def reboot(self, rbt_type='hard') -> bool:
        '''
        Reboots the PS3

        :param rbt_type str: Reboot type (soft, hard, quick, vsh)
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        if not rbt_type.lower() in ['soft', 'hard', 'quick', 'vsh']: raise InvalidParam('Reboot type is invalid')
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
        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
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
        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif led_clr == None or not led_clr in [0, 1, 2]: raise InvalidParam('Invalid LED code') 
        elif led_mode == None or not led_mode in [0, 1, 2, 3, 4, 5, 6]: raise InvalidParam('Invalid LED mode')
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

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif buzz_mode == None or not buzz_mode in [1, 2,3]: raise InvalidParam('Invalid buzz mode') 
        
        else:
            try:
                return self.get(f'http://{Core.ps3ip}/buzzer.ps3mapi?mode={str(buzz_mode)}') # buzz endpoint
            except Exception:
                return False
            
    def notify(self, noti_type=1, noti_msg='', snd_type=5, bottom=False) -> bool:
        '''
        Sends a notification to the PS3

        :param noti_type int: Notification type (0-50)
        :param noti_msg str: Message to send
        :param snd_type int: Sound to play when showing the notification (0-9)
        :param bottom bool: Wether to show the message at the bottom
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif not noti_type in [x for x in range(51)] or type(noti_type) != int: raise InvalidParam('Notification type should be integer, and between 0 and 50')
        elif type(noti_msg) != str: raise InvalidParam('Notification message should be string')
        elif not snd_type in [x for x in range(10)] or type(snd_type) != int: raise InvalidParam('Notification sound should be integer, and between 0 and 9')
        else:
            try:
                path = 'popup.ps3' if len(noti_msg) == 0 else \
                        f'popup.ps3?{noti_msg}&icon={str(noti_type)}&snd={str(snd_type)}' if not bottom else \
                            f'popup.ps3*{noti_msg}' # shows system information if no message is supplied

                return self.get(f'http://{Core.ps3ip}/{path}')

            except Exception:
                return False

    def getConsoleInfo(self) -> ResultSet: # get the console info
        '''
        Gets the PS3 information, and returns it in a JSON object
        
        :return dict: The JSON object holding all the data'''
        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
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

        if div == None: raise ParamIsNone('Div is none!')
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

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
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

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif speed == None or not str(speed).isdigit(): raise ParamIsNone('Speed has to be integer!')
        else:
            return self.get(f'http://{Core.ps3ip}/cpursx.ps3?/sman.ps3?/cpursx.ps3?fan={str(speed)}')
    
    def ejectCD(self) -> bool:
        '''
        Ejects the CD out of the tray

        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        else:
            return self.get(f'http://{Core.ps3ip}/eject.ps3')
    
    def exitToXMB(self) -> bool:
        '''
        Exits the game to the XMB screen

        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        else:
            return self.get(f'http://{Core.ps3ip}/xmb.ps3$exit')
    
    def reloadPS3Game(self) -> bool:
        '''
        Exits, and re-enters the game

        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        else:
            return self.get(f'http://{Core.ps3ip}/xmb.ps3$reloadgame')

    def getGameName(self) -> str:
        '''
        Gets the current game name (XMB Menu if no game is being played)

        :return str: Returns the game name
        '''
    
        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
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

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
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

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        else:
            try:
                procs = self.getProclist()
                procs_list = {}

                for proc in re.findall(r'\<option value\=\"(.*?)\<option value\=', ''.join(procs)):

                    pid, proc_name = proc.split('"/>')

                    if proc_name.startswith('01000300') or proc_name.startswith('01000400'): pass # if its a system process, skip
                    else: procs_list.update({pid: proc_name})
                
                if len(procs_list) <= 0:
                    return 'No processes found.'

                return procs_list if not gameonly else list(procs_list)[0]
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

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif process == None: raise ParamIsNone('Process can\'t be none!')
        elif patch_addr == None: raise ParamIsNone('Patch address can\'t be none!')
        elif hex_value == None: raise ParamIsNone('Hex value can\'t be none!')
        else:
            process = f'0x{process}' if not process.startswith('0x') else process
            hex_value = self.clean(hex_value)
            try:

                if type(patch_addr) == list:
                    for addr in patch_addr:
                        req = requests.get(f'http://{Core.ps3ip}/setmem.ps3mapi?proc={process}&addr={self.clean(addr)}&val={hex_value}')
                        if req.status_code == 200: continue
                        else: raise InvalidHTTPResponse( f'Got status code {str(req.status_code)} as response, which means "{self.HTTP_RESPONSE_CODES[req.status_code]}".')
                    return True
                else:
                    return self.get(f'http://{Core.ps3ip}/setmem.ps3mapi?proc={process}&addr={patch_addr}&val={hex_value}')

            except Exception:
                raise MemWriteException('Failed to write to console memory')
    
    def memView(self, process=None, read_addr=None, pretty=False) -> str | list:
        '''
        Shows the process memory of the specified read address
        
        :param process str: The process to read from
        :param read_addr str: The patch address to read from
        :param pretty bool: Wether to show it really pretty, or return a raw list
        :return str/list: string if `pretty` has been set to True else list
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif process == None: raise ParamIsNone('Process can\'t be none!')
        elif read_addr == None: raise ParamIsNone('Read address can\'t be none!')
        else:
            try:
                read_addr = self.clean(read_addr)
                process = f'0x{process}' if not process.startswith('0x') else process

                page = requests.get(f'http://{Core.ps3ip}/getmem.ps3mapi?proc={process}&addr={read_addr}&len=256')
                memview = re.findall(r'\<font color=\#ff0\>\<\/font\>\<hr\>(.*?)\<textarea id=\"output\"', page.text)[0].split('<br>') 

                return memview if not pretty \
                    else '\n'.join(memview)

            except Exception:
                raise MemReadException('Failed to read from console memory')
    
    def memRead(self, process=None, read_addr=None) -> str:
        '''
        Reads from a specific address
        
        :param process str: The process to read from
        :param read_addr str: The patch address to read from
        :return str: memory value
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif process == None: raise ParamIsNone('Process can\'t be none!')
        elif read_addr == None: raise ParamIsNone('Read address can\'t be none!')
        else:
            try:
                process = f'0x{process}' if not process.startswith('0x') else process
                read_addr = self.clean(read_addr)
                
                page = requests.get(f'http://{Core.ps3ip}/getmem.ps3mapi?proc={process}&addr={read_addr}&len=256')
                memview = re.findall(r'\<textarea id=\"output\" style=\"display\:none\"\>(.*?)\<\/textarea\>', page.text)
                return memview[0]

            except Exception:
                raise MemReadException('Failed to read from console memory')
        
    def uploadFile(self, local_path=None, destination=None, filename=None, isbyte=False) -> bool:
        '''
        Uploads a local file
        
        :param local_path str: Location of the file to be uploaded
        :param destination str: Destination of file
        :param filename str: Name of the file to be saved as
        :param isbyte bool: Wether we should open the file in `Read Bytes` mode
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif local_path == None: raise ParamIsNone('Local path can\'t be none!')
        elif destination == None: raise ParamIsNone('Destination can\'t be none!')
        elif filename == None: raise ParamIsNone('Filename can\'t be none!')
        elif type(isbyte) != bool: raise InvalidParam('IsByte parameter has to be bool!')
        else:
            try:
                with open(local_path, 'rb' if isbyte else 'r', buffering=(16*1024*1024)) as fd:
                    parsed_content = fd.read(1024*1024).replace('\n', '|').replace('\r\n', '|') # replaces newlines with "|" because that is the line seperator

                req = None
                try:
                    req = requests.get(f'http://{Core.ps3ip}/write.ps3/{destination.strip()}/{filename}&t={parsed_content}') # since webman responds with 1225 if it uploaded, our helper function won't help
                except requests.RequestException: pass

                return req.status_code == 1225 if not req == None else True
            except Exception:
                raise MemWriteException('Failed to upload file')
