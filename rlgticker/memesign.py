import serial
import serial.tools.list_ports
from time import sleep as slp

'''
        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
'''


def get_port(verbose=False, auto=True):
    """
    Returns a selected com port, or automatically finds one with arduino in the port description.
    :param verbose: Provides full port description including number, description, and location when auto=False
    :param auto:    Automatically returns the port for the first device containing arduino in the port description
    :return:        Com port string to attempt to connect to. Formatted as 'COM2', or 'COM3', etc.
    """
    ports = list(serial.tools.list_ports.comports())
    if auto:
        for p in ports:
            if "arduino" in p[1].lower():
                return p[0]
    else:
        ind = 1
        for p in ports:
            if verbose:
                print('{:d}: '.format(ind) + (', '.join([str(i) for i in p])))
            else:
                print('{:d}: '.format(ind) + p[1])
            ind += 1
        return ports[int(input("Select port number index\n>>> "))]


class MemeSign:
    def __init__(self, autocom=True):
        self.memes = []
        self.num_memes = 0
        self.ser = serial.Serial(get_port(auto=autocom), 9600)

    def add_meme(self, new_meme):
        """
        Adds a string to the list of memes received.
        :param new_meme: A string containing a new dank meme.
        :return: None
        """
        self.memes.append(new_meme)

    def get_meme(self, index=None):
        """
        Returns a specified meme string or the last meme received if no index is provided.
        :param index: retrieve the meme stored at this index in self.memes
        :return: last string stored in self.memes, or string at a specific index.
        """
        if not index:
            return self.memes[-1]
        else:
            return self.memes[index]

    def get_num_memes(self):
        """
        used to get the number of memes stored so far
        :return: number of strings in self.memes
        """
        return len(self.memes)

    def print_meme(self, index=None):
        """
        Sends a meme over a serial connection encoded in ascii
        :param index: Optional identifier for
        :return: none
        """
        if not index:
            self.ser.write((self.memes[-1] + '\n').encode('ascii', errors='ignore'))
        else:
            self.ser.write((self.memes[index] + '\n').encode('ascii', errors='ignore'))

    def wait(self):
        """
        Used as an indicator for when the sign is ready to receive another post string, based on reading the incoming
        serial buffer.
        :return: True if waiting, False if ready for a new string.
        """
        if not self.ser.inWaiting() > 0:
            return True
        else:
            self.ser.flushInput()
            slp(0.04)   # Required to prevent post strings from chaining together on the display
            return False
