import requests
from bs4 import BeautifulSoup

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
# (C) 2021-2021 PyPS3 by Nexus                                 #
# (C) 2010-2021 multiMAN/webMAN/sMAN/sLaunch/prepNTFS by DeanK #
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

class API:
    def __init__(self):
        self.HTTP_RESPONSE_CODES = {
            # 1xx informational response
            100: 'Continue',
            101: 'Switching Protocols',
            102: 'Processing',
            103: 'Early Hints',

            # 2xx success,
            200: 'OK',
            201: 'Created',
            202: 'Accepted',
            203: 'Non-Authoritative Information',
            204: 'No Content',
            205: 'Reset Content',
            206: 'Partial Content',
            207: 'Multi-Status',
            208: 'Already Reported',
            226: 'IM Used',

            # 3xx redirection
            300: 'Multiple Choices',
            301: 'Moved Permanently',
            302: 'Found',
            303: 'See Other',
            304: 'Not Modified',
            305: 'Use Proxy',
            306: 'Switch Proxy',
            307: 'Temporary Redirect',
            308: 'Permanent Redirect',

            # 4xx client errors, you fucked up
            400: 'Bad Request',
            401: 'Unauthorized',
            402: 'Payment Required',
            403: 'Forbidden',
            404: 'Not Found',
            405: 'Method Not Allowed',
            406: 'Not Acceptable',
            407: 'Proxy Authentication Required',
            408: 'Request Timeout',
            409: 'Conflict',
            410: 'Gone',
            411: 'Length Required',
            412: 'Precondition Failed',
            413: 'Payload Too Large',
            414: 'URI Too Long',
            415: 'Unsupported Media Type',
            416: 'Range Not Satisfiable',
            417: 'Expectation Failed',
            418: 'I\'m a teapot',
            421: 'Misdirected Request',
            422: 'Unprocessable Entity',
            423: 'Locked',
            424: 'Failed Dependency',
            425: 'Too Early',
            426: 'Upgrade Required',
            428: 'Precondition Required',
            429: 'Too Many Requests',
            431: 'Request Header Fields Too Large',
            451: 'Unavailable For Legal Reasons',

            # 5xx server errors, they fucked up
            500: 'Internal Server Error',
            501: 'Not Implemented',
            502: 'Bad Gateway',
            503: 'Service Unavailable',
            504: 'Gateway Timeout',
            505: 'HTTP Version Not Supported',
            506: 'Variant Also Negotiates',
            507: 'Insufficient Storage',
            508: 'Loop Detected',
            509: 'Bandwidth Limit Exceeded',
            510: 'Not Extended',
            511: 'Network Authentication Required',
            529: 'Site is overloaded',
            530: 'Site is frozen',
            598: 'Network read timeout error',

            # CloudFlare response codes, don't know why anyone would use CF on a PS3 lol
            520: 'Web Server Returned an Unknown Error',
            521: 'Web Server Is Down',
            522: 'Connection Timed Out',
            523: 'Origin Is Unreachable',
            524: 'A Timeout Occurred',
            525: 'SSL Handshake Failed',
            526: 'Invalid SSL Certificate'
        }

    def connect(self, ps3ip=None): # check if its up
        if ps3ip == None:
            return False, 'Console IP is None.'

        else:
            try:
                re = requests.get(f'http://{ps3ip}/cpursx.ps3?/sman.ps3')
                if re.status_code == 200:
                    return True
                else:
                    return False, f'Got status code {str(re.status_code)} when connecting, which means "{self.HTTP_RESPONSE_CODES[re.status_code]}".'

            except Exception as e:
                print(f'[PyPS3] [CONNECT] [EXCEPTION] {str(e)}')
                return False, str(e)
    
    def reboot(self, ps3ip=None, type='hard'):
        if ps3ip == None or not type in ['soft', 'hard', 'quick', 'vsh']:
            return False, 'Console IP is None or Reboot Type is invalid.'

        else:
            try:
                if self.connect(ps3ip):
                    re = requests.get(f'http://{ps3ip}/reboot.ps3?{type}')
                    if re.status_code == 200:
                        return True
                    else:
                        return False, f'Got status code {str(re.status_code)} when rebooting console, which means "{self.HTTP_RESPONSE_CODES[re.status_code]}".'

                else:
                    return False, 'Console could not be found'

            except Exception as e:
                print(f'[PyPS3] [REBOOT] [EXCEPTION] {str(e)}')
                return False, str(e)
    
    def stopserver(self, ps3ip=None, type=None): # NEEDS TESTING
        if ps3ip == None or type == None:
            return False, 'Console IP/Server Type is None.'
        
        else:
            try:
                if self.connect(ps3ip):
                    re = requests.get(f'http://{ps3ip}/netstatus.ps3?{type.lower()}')
                    if not re.status_code == 200:
                        return False, f'Got status code {str(re.status_code)} when shutting down {type.upper()} server, which means "{self.HTTP_RESPONSE_CODES[re.status_code]}".'

                    if re.text == '': # FTP is enabled
                        requests.get(f'http://{ps3ip}/netstatus.ps3?stop-{type.lower()}') # Disable FTP
                        return True
                    else:
                        return False, f'{type.upper()} server is already stopped.'
                
                else:
                    return False, 'Console could not be found.'
            
            except Exception as e:
                print(f'[PyPS3] [STOPSERVER] [EXCEPTION] {str(e)}')
                return False, str(e)
    
    def shutdown(self, ps3ip=None):
        if ps3ip == None:
            return False, 'Console IP is None.'

        else:
            try:
                if self.connect(ps3ip):
                    re = requests.get(f'http://{ps3ip}/shutdown.ps3')
                    if re.status_code == 200:
                        return True
                    else:
                        return False, f'Got status code {str(re.status_code)} when shutting down console, which means "{self.HTTP_RESPONSE_CODES[re.status_code]}".'
                
                else:
                    return False, 'Console could not be found.'

            except Exception as e:
                print(f'[PyPS3] [SHUTDOWN] [EXCEPTION] {str(e)}')
                return False, str(e)
    
    def led(self, ps3ip=None, led_clr=None, led_mode=None):
        if ps3ip == None or led_clr == None or led_mode == None\
        or not led_clr in [0, 1, 2] or not led_mode in [0, 1, 2, 3, 4, 5, 6]:
            return False, 'Console IP/LED Color/LED Mode is None or LED Color/LED Mode is invalid.'
        
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
                
                if self.connect(ps3ip):
                    re = requests.get(f'http://{ps3ip}/led.ps3mapi?color={led_clr}&mode={led_mode}')
                    if re.status_code == 200:
                        return True
                    else:
                        return False, f'Got status code {str(re.status_code)} when setting LED, which means "{self.HTTP_RESPONSE_CODES[re.status_code]}".'

                else:
                    return False, 'Console could not be found.'

            except Exception as e:
                print(f'[PyPS3] [LED] [EXCEPTION] {str(e)}')
                return False, str(e)
    
    def buzz(self, ps3ip=None, mode=1):
        if ps3ip == None or mode not in [1, 2, 3]:
            return False, 'Console IP is None or Mode is invalid.'
        
        else:
            try:
                if self.connect(ps3ip):
                    # once = 1
                    # twice = 2
                    # triple = 3

                    re = requests.get(f'http://{ps3ip}/buzzer.ps3mapi?mode={str(mode)}') # buzz endpoint
                    if re.status_code == 200:
                        return True
                    else:
                        return False, f'Got status code {str(re.status_code)} when buzzing, which means "{self.HTTP_RESPONSE_CODES[re.status_code]}".'

                else:
                    return False, 'Console could not be found.'

            except Exception as e:
                print(f'[PyPS3] [BUZZ] [EXCEPTION] {str(e)}')

    def getconsoleinfo(self, ps3ip=None): # get the console info
        if ps3ip == None:
            return False, 'Console IP is None.'
        
        else:
            if self.connect(ps3ip):
                try:
                    re = requests.get(f'http://{ps3ip}/cpursx.ps3?/sman.ps3')

                    if re.status_code == 200:
                        soup = BeautifulSoup(re.text.encode('utf-8'), 'html.parser')
                        return soup.findAll('a', attrs={'class': 's'})
                    else:
                        return False, f'Got status code {str(re.status_code)} when getting console info, which means "{self.HTTP_RESPONSE_CODES[re.status_code]}".'
                
                except Exception as e:
                    print(f'[PyPS3] [GETCONSOLEINFO] [EXCEPTION] {str(e)}')
                    return False, str(e)
            else:
                return False, 'Console could not be found.'
    
    def getfirmware(self, div=None):
        if div == None:
            return False, 'Div is None.'
        
        else:
            try:
                clutter = div[4].text
                firmware = ''

                for l in clutter: 
                    if l != "P": firmware += l
                    else: break
                
                if firmware == None:
                    return False, 'Console returned empty firmware.'

                else:
                    return firmware.split(': ', 1)[1]
            
            except Exception as e:
                print(f'[PyPS3] [GETFIRMWARE] [EXCEPTION] {str(e)}')
                return False, str(e)
    
    def getcurrentgame(self, div=None):
        if div == None:
            return False, 'Div is None'

        else:
            try:
                soup = BeautifulSoup(div.text, 'html.parser')
                strings = soup.findAll('h2')
                res = strings[0].text
                game = None

                if res.startswith('BL') or res.startswith('NP') or res.startswith('BC'):
                    game = res.split(' ', 1)[1].encode('ascii', 'ignore').decode()

                else: 
                    game = 'XMB Menu'
                
                return game

            except Exception as e:
                print(f'[PyPS3] [GETCURRENTGAME] [EXCEPTION] {str(e)}')
                return False, str(e)


    def memwrite(self, ps3ip=None, process=None, patch_addr=None, hex_code=None): # write to memory
        if ps3ip == None \
        or process == None \
        or patch_addr == None \
        or hex_code == None:
            return False, 'Console IP/Process/Patch Address/Hex Code is None.'

        else:
            try:
                re = requests.get(f'http://{ps3ip}/setmem.ps3mapi?proc={process}&addr={patch_addr}&val={hex_code}')
                if re.status_code == 200:
                    return True
                else:
                    return False, f'Got status code {str(re.status_code)} when writing to memory, which means "{self.HTTP_RESPONSE_CODES[re.status_code]}".'

            except Exception as e:
                print(f'[PyPS3] [MEMWRITE] [EXCEPTION] {str(e)}')
                return False, str(e)