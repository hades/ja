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

class People(object):
    def __init__(self):
        self.list = []
        self.by_contact_id = {}
        self.by_name = {}

    def add(self, person):
        self.list.append(person)
        for contact in person.contacts:
            self.by_contact_id[(contact.source, contact.id)] = person
        if person.name not in self.by_name:
            self.by_name[person.name] = []
        self.by_name[person.name].append(person)

    def add_contact(self, contact, connection):
        if (contact.source, contact.id) in self.by_contact_id:
            for old_contact in self.by_contact_id[(contact.source, contact.id)]:
                if old_contact.source == contact.source and old_contact.id == contact.id:
                    old_contact.connections.add(connection)

class Person(object):
    def __init__(self):
        self.name = ''
        self.contacts = set()

    def add_contact(self, contact):
        self.contacts.add(contact)
        if not self.name:
            self.name = contact.name

class Contact(object):
    def __init__(self, id, source):
        self.id = id
        self.source = source
        self.name = str(id)
        self.connections = set()
        self.groups = set()

    def __eq__(self, other):
        return self.id == other.id and self.source == other.source

    def __hash__(self):
        return hash((self.id, self.source))

# vim:sw=4:ts=4:et
