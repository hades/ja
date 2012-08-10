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

from ja.core import command, ja
from ja.plugins import Plugin

from ja.plugins.xmpp.connection import XmppConnection

class XmppPlugin(Plugin):
    def __init__(self):
        super().__init__("xmpp")
        self.ja = ja()

    @command
    def connect(self, arg):
        if not arg:
            self.ja.print("xmpp: please specify JID to connect to")
            return
        connection = XmppConnection(arg)
        self.ja.add_connection(connection)
        connection.connect()

# vim:sw=4:ts=4:et
