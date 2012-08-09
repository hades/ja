# Copyright 2012 Edward Toroshchin <ja-project@hades.name>
#
# This is ja, the console IM client.
#
# ja is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ja is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See the full text of the GNU General Public License in the COPYING
# file in source code directory.
#
# If you are unable to read that file, see <http://www.gnu.org/licenses/>.
#

from datetime import datetime
from urwid import *

from ja import __version__ as version
from ja.widgets import SystemMessagesWidget

DEBUG   = -1
TWITTER = 0
RANT    = 1
ANXIETY = 2
FRUSTRE = 3
PANIC   = 4

class Ja(object):
    def __init__(self, storage):
        self.storage = storage
        self.log = []
        self.print("This is ja version {}".format(version))
        self.print("Copyright © 2012 Edward Toroshchin <ja-project@hades.name>")

    def __setup_ui(self):
        self.chatview = SystemMessagesWidget(self)
        self.inputview = Edit("> ")
        self.view = Frame(self.chatview, footer=self.inputview, focus_part='footer')
        self.loop = MainLoop(self.view, unhandled_input=self.keypress)

    def keypress(self, key):
        raise ExitMainLoop()

    def print(self, text, level=TWITTER):
        self.log.append((datetime.now(), level, text))

    def run(self, args):
        self.__setup_ui()
        return self.loop.run()

def ja(*args, **kwargs):
    if not hasattr(ja, 'instance'):
        ja.instance = Ja(*args, **kwargs)
    return ja.instance

# vim:sw=4:ts=4:et
