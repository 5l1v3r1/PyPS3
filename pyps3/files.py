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
Submodule which holds all functions regarding files, directories and whatever
'''

import requests
from pyps3.src.exceptions import *
from pyps3.src.core import Core
from pyps3.misc import Misc

class Files():
    def __init__(self):
        pass

    def uploadFile(self, local_path=None, destination=None, filename=None, isbyte=False, restart_after=False) -> bool:
        '''
        Uploads a local file
        
        :param local_path str: Location of the file to be uploaded
        :param destination str: Destination of file
        :param filename str: Name of the file to be saved as
        :param isbyte bool: Wether we should open the file in `Read Bytes` mode
        :param restart_after bool: Restart the playstation after it has succeeded
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif local_path == None: raise ParamIsNone('Local path can\'t be none!')
        elif destination == None: raise ParamIsNone('Destination can\'t be none!')
        elif filename == None: raise ParamIsNone('Filename can\'t be none!')
        elif type(isbyte) != bool: raise InvalidParam('Isbyte parameter has to be bool!')
        elif type(restart_after) != bool: raise InvalidParam('restart_after parameter has to be bool!')
        else:
            try:
                with open(local_path, 'rb' if isbyte else 'r', buffering=(16*1024*1024)) as fd:
                    parsed_content = fd.read(1024*1024).replace('\n', '|').replace('\r\n', '|') # replaces newlines with "|" because that is the line seperator

                req = None
                try:
                    req = requests.get(f'http://{Core.ps3ip}/write.ps3/{destination.strip()}/{filename}&t={parsed_content}') # since webman responds with 1225 if it uploaded, our helper function won't help
                except requests.RequestException: pass

                if restart_after:
                    Misc().reboot()

                return req.status_code == 1225 if not req == None else True
            except Exception:
                raise MemWriteException('Failed to upload file')
    
    def deleteFile(self, file_path=None, restart_after=False) -> bool:
        '''
        Removes a file from the PS3

        :param file_path str: Location of the file to be erased
        :param restart_after bool: Restart the playstation after it has succeeded
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif file_path == None: raise ParamIsNone('file path can\'t be none!')
        elif type(restart_after) != bool: raise InvalidParam('restart_after parameter has to be bool!')
        else:
            try:

                req = requests.get(f'http://{Core.ps3ip}/delete.ps3/{file_path.strip()}')

                if restart_after:
                    Misc().reboot()

                return req.status_code == 200
            except Exception:
                raise MemWriteException('Failed to remove file/directory')
    
    def rename(self, old_path=None, new_path=None, restart_after=False) -> bool:
        '''
        Renames/moves a file/directory

        :param old_path str: Old path
        :param new_path str: New path
        :param restart_after bool: Restart the playstation after it has succeeded
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif old_path == None: raise ParamIsNone('Old path can\'t be none!')
        elif new_path == None: raise ParamIsNone('New path can\'t be none!')
        elif type(restart_after) != bool: raise InvalidParam('restart_after parameter has to be bool!')
        else:
            try:

                req = requests.get(f'http://{Core.ps3ip}/rename.ps3/{old_path}|{new_path}')

                if restart_after:
                    Misc().reboot()

                return req.status_code == 200
            except Exception:
                raise MemWriteException('Failed to rename file/directory')
    
    def move(self, old_path=None, new_path=None, restart_after=False) -> bool:
        '''
        Moves a file/directory from old_path to new_path

        :param old_path str: Old path
        :param new_path str: New path
        :param restart_after bool: Restart the playstation after it has succeeded
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif old_path == None: raise ParamIsNone('Old path can\'t be none!')
        elif new_path == None: raise ParamIsNone('New path can\'t be none!')
        elif type(restart_after) != bool: raise InvalidParam('restart_after parameter has to be bool!')
        else:
            try:

                req = requests.get(f'http://{Core.ps3ip}/move.ps3/{old_path}|{new_path}')

                if restart_after:
                    Misc().reboot()

                return req.status_code == 200
            except Exception:
                raise MemWriteException('Failed to move file/directory')
    
    def mkDir(self, dir_path=None, restart_after=False) -> bool:
        '''
        Creates a directory
        
        :param dir_path str: Where the directory should be created
        :param restart_after bool: Restart the playstation after it has succeeded
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif dir_path == None: raise ParamIsNone('Directory path can\'t be none!')
        elif type(restart_after) != bool: raise InvalidParam('restart_after parameter has to be bool!')
        else:
            try:
                req = requests.get(f'http://{Core.ps3ip}/mkdir.ps3/{dir_path}')

                if restart_after:
                    Misc().reboot()

                return req.status_code == 200
            except Exception:
                raise MemWriteException('Failed to create directory')
    
    def rmDir(self, dir_path=None, restart_after=False) -> bool:
        '''
        Removes a directory
        
        :param dir_path str: Which directory should be removed
        :param restart_after bool: Restart the playstation after it has succeeded
        :return bool: True, False
        '''

        if Core.ps3ip == None: raise ConsoleNotFound('Please connect first')
        elif dir_path == None: raise ParamIsNone('Directory path can\'t be none!')
        elif type(restart_after) != bool: raise InvalidParam('restart_after parameter has to be bool!')
        else:
            try:
                req = requests.get(f'http://{Core.ps3ip}/delete.ps3/{dir_path}') # we use "/delete.ps3" because "/rmdir.ps3" only removes empty folders

                if restart_after:
                    Misc().reboot()

                return req.status_code == 200
            except Exception:
                raise MemWriteException('Failed to create directory')