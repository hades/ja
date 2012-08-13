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
    def __init__(self, ja, message=None, contact=None):
        self.widget = None
        self.messages = []
        self.ja = ja
        self.contact = None
        self.connection = None
        self.resource = None
        if message:
            self.messages.append(message)
            self.contact = message.contact
            self.connection = message.connection
            self.resource = message.resource
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

    def select_contact(self):
        if self.contact:
            return self.contact

    def select_connection(self, contact):
        if self.connection and self.connection.connected:
            return self.connection
        return self.ja.select_connection(contact)

    def select_resource(self, connection, contact):
        return connection.select_resource(contact, self.resource)

    def send(self, message):
        contact = self.select_contact()
        if not contact:
            return
        connection = self.select_connection(contact)
        if not connection:
            return
        resource = self.select_resource(connection, contact)
        connection.send_message(contact, resource, message)

# vim:sw=4:ts=4:et
