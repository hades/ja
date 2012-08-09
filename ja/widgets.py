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

from urwid import *

class SystemMessagesWalker(ListWalker):
    def __init__(self, ja):
        self.ja = ja
        self.focus = 0
        self.lines = []

    def get_focus(self):
        return self._get_at(self.focus)

    def set_focus(self, focus):
        self.focus = focus
        self._modified()

    def get_next(self, position):
        return self._get_at(position + 1)

    def get_prev(self, position):
        return self._get_at(position - 1)

    def _get_at(self, index):
        if index < 0:
            return None, None

        if index >= len(self.lines):
            for i in range(len(self.lines), len(self.ja.log)):
                self.lines.append(self._format(self.ja.log[i]))

        if index >= len(self.lines):
            return None, None

        return self.lines[index], index

    def _format(self, message):
        text = ">>> {0[2]}".format(message)
        return Text(text)

class MessagesWidget(ListBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SystemMessagesWidget(MessagesWidget):
    def __init__(self, ja):
        super().__init__(SystemMessagesWalker(ja))
