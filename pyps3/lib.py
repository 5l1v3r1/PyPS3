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
Main module for connecting
'''

import requests, re
from bs4 import BeautifulSoup

from pyps3.src.exceptions import *
from pyps3.src.core import Core
from pyps3.src.utils import Utils
from pyps3.misc import Misc

class API():
    def __init__(self):
        pass

    def connect(self, ps3ip=None, notify=False) -> bool: # check if its up
        '''
        Connecs to the PS3

        :param ps3ip str: The Console IP address to connect to
        :param notify bool: Wether to show a notification on the PS3
        :return bool: True, False
        '''

        if ps3ip == None: raise ConsoleNotFound('Please enter a valid Playstation target IP')
        else:
            try:
                

                if Utils().get(f'http://{ps3ip}/index.ps3'):
                    Core.ps3ip = ps3ip

                    if notify:
                        Misc().notify(20, 'PyPS3: Connected!', 4)
                        Misc().buzz(2)

                    return True

            except Exception:
                raise ConsoleConnectionError('Failed to connect to the PS3')

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

                    if res.startswith('BL') or res.startswith('NP') or res.startswith('BC'): game = res.split(' ', 1)[1].decode()
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
        Gets the running processes, returns the game process by default
        
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
                    procs_list.update({pid: proc_name})
                
                if len(procs_list) <= 0:
                    return 'No processes found.'

                return procs_list if not gameonly else list(procs_list)[0]
            except Exception:
                raise GetProcsException('Failed to parse games')