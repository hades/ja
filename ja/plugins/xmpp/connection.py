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

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

from ja.connection import Connection
from ja.core import ja

class XmppConnection(Connection):
    def __init__(self, jid):
        self.ja = ja()
        self.jid = jid
        self.password = ''
        self.client = None

    def connect(self, password=None):
        if password:
            self.password = password
            if self.client:
                self.client.password = password
        if not self.password:
            self.ja.ask_password("Password for {}".format(self.jid), self.connect)
            return
        if not self.client:
            self.client = ClientXMPP(self.jid, self.password)
            self.client.add_event_handler('connected', self._handle_connected)
            self.client.add_event_handler('disconnected', self._handle_disconnected)
        self.client.connect()
        self.client.process(block=False)

    def disconnect(self):
        self.client.disconnect(wait=True)

    def _handle_connected(self, data):
        self.ja.print("xmpp: connected to JID {}".format(self.jid))

    def _handle_disconnected(self, data):
        self.ja.print("xmpp: JID {} disconnected".format(self.jid))

# vim:sw=4:ts=4:et
