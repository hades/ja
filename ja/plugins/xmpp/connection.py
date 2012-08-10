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
from ja.people import Contact

def reconnect_on_timeout(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except IqTimeout:
            self.ja.print("xmpp: request timed out, reconnecting")
            self.disconnect()
            self.connect()
    wrapper.__doc__ = func.__doc__
    wrapper.__module__ = func.__module__
    wrapper.__name__ = func.__name__
    return wrapper

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
            self.client.add_event_handler('session_start', self._handle_session_start)
            self.client.add_event_handler('disconnected', self._handle_disconnected)
        self.client.connect()
        self.client.process(block=False)

    def disconnect(self):
        self.client.disconnect(wait=True)

    def _handle_disconnected(self, data):
        self.ja.print("xmpp: JID {} disconnected".format(self.jid))

    @reconnect_on_timeout
    def _handle_session_start(self, data):
        self.ja.print("xmpp: connected to JID {}".format(self.jid))
        try:
            self._parse_roster(self.client.get_roster()['roster'])
        except IqError as e:
            self.ja.print("xmpp: error retrieving roster {}".format(e))

    def _parse_roster(self, roster):
        roster = roster.get_items()
        for item in roster:
            contact = Contact(item, 'xmpp')
            if 'name' in roster[item]:
                contact.name = roster[item]['name']
            if 'groups' in roster[item]:
                contact.groups = set(roster[item]['groups'])
            self.ja.add_contact(contact, self)

# vim:sw=4:ts=4:et
