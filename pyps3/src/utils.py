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
Submodule for all misc/helper functions
'''

import requests
from pyps3.src.exceptions import *
from pyps3.src.core import Core

class Utils():
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