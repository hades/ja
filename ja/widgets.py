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

class MessagesWalker(ListWalker):
    def __init__(self):
        self.last = 0

    def get_focus(self):
        return self._get_at(self.last)

    def set_focus(self, focus):
        return None

    def get_next(self, position):
        return self._get_at(position + 1)

    def get_prev(self, position):
        return self._get_at(position - 1)

    def _get_at(self, index):
        return None, None


class SystemMessagesWalker(MessagesWalker):
    def __init__(self, ja):
        self.ja = ja
        self.lines = []
        super().__init__()

    def _format(self, message):
        text = Text(">>> {0[2]}".format(message))
        return text

    def _get_at(self, index):
        if index < 0:
            return None, None

        if index >= len(self.lines):
            for i in range(len(self.lines), len(self.ja.log)):
                self.lines.append(self._format(self.ja.log[i]))
            self.last = len(self.lines) - 1

        if index >= len(self.lines):
            return None, None

        return self.lines[index], index

class ChatWalker(MessagesWalker):
    def __init__(self, chat):
        self.chat = chat
        self.lines = []
        self.histlines = []
        super().__init__()

    def _format(self, message):
        text = Text("{0.text}".format(message))
        return text

    def _get_at(self, index):
        lines = self.lines
        lindex = index
        direction = 1
        if index < 0:
            lines = self.histlines
            lindex = -index
            direction = -1

        if lindex >= len(lines):
            cindex = len(lines)
            while cindex <= lindex:
                msg = self.chat.message(cindex * direction)
                if not msg:
                    return None, None
                lines.append(self._format(msg))
                cindex += 1
            self.last = len(self.lines) - 1

        if lindex >= len(lines):
            return None, None

        return lines[lindex], index

class MessagesWidget(ListBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        self._invalidate()

class SystemMessagesWidget(MessagesWidget):
    def __init__(self, ja):
        super().__init__(SystemMessagesWalker(ja))

class ChatWidget(MessagesWidget):
    def __init__(self, chat):
        super().__init__(ChatWalker(chat))

# vim:sw=4:ts=4:et
