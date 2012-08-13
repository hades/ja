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

class Message(object):
    def __init__(self, contact, connection, text, resource=None):
        self.contact = contact
        self.connection = connection
        self.text = text
        self.resource = resource

class Chat(object):
    def __init__(self, message=None, contact=None):
        self.widget = None
        self.messages = []
        self.contact = None
        if message:
            self.messages.append(message)
            self.contact = message.contact
        elif contact:
            self.contact = contact

    def message(self, index):
        if index >= 0:
            try:
                return self.messages[index]
            except IndexError:
                return None

    def accept_message(self, message):
        if message.contact == self.contact:
            self.messages.append(message)
            if self.widget:
                self.widget.update()
            return True
        return False

# vim:sw=4:ts=4:et
