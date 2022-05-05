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

'''
Submodule with misc functions
'''

import requests, re

from pyps3.src.exceptions import *
from pyps3.src.core import Core
from pyps3.src.utils import Utils

class Misc():
    def __init__(self):
        pass

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

                return Utils().get(f'http://{Core.ps3ip}/{path}')

            except Exception:
                return False
    
    def getFirmware(self) -> str:
        '''
        Parses the firmware from the page

        :return str: Returns the console firmware
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        else:
            try:
                page = requests.get(f'http://{Core.ps3ip}/cpursx.ps3?/sman.ps3')
                firmware = re.findall(r'href\=\"\/setup\.ps3\"\>Firmware\: (.*?)\<br\>\<br\>', page.text)
                
                if firmware == None or len(firmware) == 0: raise EmptyFirmwareResponse('Console returned empty firmware.')
                else: return firmware[0]
            
            except Exception:
                raise GetFirmwareException('Unable to parse firmware')
    
    def getTemps(self) -> dict:
        '''
        Gets the consoles temperature

        :return dict: Returns the CPU, RSX and max temperature
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        else:
            page = requests.get(f'http://{Core.ps3ip}/cpursx_ps3').text
            cpu, rsx = re.findall(r'CPU: (.*?)°C \| RSX: (.*?)°C', page)[0]

            return {'cpu': cpu, 'rsx': rsx}
    
    def setFanSpeed(self, speed: None) -> bool:
        '''
        Sets the fan speed (in %)

        :param speed int: The fan speed (in %)
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif speed == None or not str(speed).isdigit(): raise ParamIsNone('Speed has to be integer!')
        else:
            return Utils().get(f'http://{Core.ps3ip}/cpursx.ps3?fan={str(speed)}')
    
    def ejectCD(self) -> bool:
        '''
        Ejects the CD out of the tray

        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        else:
            return Utils().get(f'http://{Core.ps3ip}/eject.ps3')
    
    def exitToXMB(self) -> bool:
        '''
        Exits the game to the XMB screen

        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        else:
            return Utils().get(f'http://{Core.ps3ip}/xmb.ps3$exit')
    
    def reloadPS3Game(self) -> bool:
        '''
        Exits, and re-enters the game

        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        else:
            return Utils().get(f'http://{Core.ps3ip}/xmb.ps3$reloadgame')

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
                
                return Utils().get(f'http://{Core.ps3ip}/led.ps3mapi?color={str(led_clr)}&mode={str(led_mode)}')
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
                return Utils().get(f'http://{Core.ps3ip}/buzzer.ps3mapi?mode={str(buzz_mode)}') # buzz endpoint
            except Exception:
                return False
    
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
                return Utils().get(f'http://{Core.ps3ip}/reboot.ps3?{type}')
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
                return Utils().get(f'http://{Core.ps3ip}/shutdown.ps3')
            except Exception:
                raise ShutdownException('Failed to shit down')