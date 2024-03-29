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

import sys

from datetime import datetime
from threading import Lock
from urwid import *

from ja import __version__ as version
from ja.chat import Chat
from ja.logging import setupLogging
from ja.people import People
from ja.widgets import SystemMessagesWidget, ChatWidget

DEBUG   = -1
TWITTER = 0
RANT    = 1
ANXIETY = 2
FRUSTRE = 3
PANIC   = 4

def command(func):
    func.__command = True
    return func

def threadprotect(func):
    def wrapper(self, *args, **kwargs):
        self._lock.acquire()
        res = func(self, *args, **kwargs)
        self._lock.release()
        return res
    wrapper.__doc__ = func.__doc__
    wrapper.__module__ = func.__module__
    wrapper.__name__ = func.__name__
    return wrapper

def redraw_screen(func):
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        if hasattr(self, 'loop'):
            self.loop.draw_screen()
        return res
    wrapper.__doc__ = func.__doc__
    wrapper.__module__ = func.__module__
    wrapper.__name__ = func.__name__
    return wrapper

class Ja(object):
    def __init__(self, storage):
        self._lock = Lock()
        self.storage = storage
        self.log = []
        self.password_cb = []
        self.plugins = {}
        self.commands = {}
        self.connections = []
        self.exiting = False
        self.people = People()
        self.chats = []
        self.current_chat = None
        self.print("This is ja version {}".format(version))
        self.print("Copyright © 2012 Edward Toroshchin <ja-project@hades.name>")

    @threadprotect
    def __input(self):
        input = self.inputview.get_edit_text()
        self.inputview.set_edit_text("")
        return input

    def __setup_ui(self):
        self.sysview = SystemMessagesWidget(self)
        self.inputview = Edit("> ")
        self.view = Frame(self.sysview, footer=self.inputview, focus_part='footer')
        self.loop = MainLoop(self.view, unhandled_input=self.keypress)
        setupLogging(self)
        self.__update_inputview()

    def __setup_commands(self):
        for p in dir(self):
            if getattr(getattr(self, p), '__command', False):
                self.add_command(p, getattr(self, p))
        for pname in self.plugins:
            plugin = self.plugins[pname]
            self.__setup_plugin_commands(plugin, pname)

    def __setup_plugin_commands(self, plugin, pname):
        for cn in dir(plugin):
            cc = getattr(plugin, cn)
            if getattr(cc, '__command', False):
                self.add_command("{}.{}".format(pname, cn), cc)

    @threadprotect
    @redraw_screen
    def __refresh_sysview(self):
        try:
            self.sysview.update()
        except AttributeError:
            pass

    @threadprotect
    def __update_inputview(self):
        if self.password_cb:
            self.inputview.set_caption("{}: ".format(self.password_cb[-1][0]))
        else:
            self.inputview.set_caption("> ")

    def add_command(self, name, proc):
        if name in self.commands:
            self.print("command {} conflicts with existing command".format(name))
        else:
            self.commands[name] = proc

    def add_connection(self, connection):
        self.connections.append(connection)

    def add_contact(self, contact, connection):
        self.people.add_contact(contact, connection)

    def ask_password(self, question, callback):
        self.password_cb.insert(0, (question, callback))
        self.__update_inputview()

    def execute(self, lines):
        if self.password_cb:
            question, cb = self.password_cb.pop()
            cb(lines)
            self.__update_inputview()
            return
        if lines.startswith('/'):
            args = lines[1:].split(' ', 1)
            command = args[0]
            arg = args[1] if len(args) > 1 else None
            if command in self.commands:
                try:
                    self.commands[command](arg)
                except Exception as e:
                    self.print("error executing command {}: {}".format(command, type(e)))
                    raise
            else:
                self.print("unknown command {}".format(command))
        else:
            if not self.current_chat:
                self.print("this is not a chat window")
            else:
                self.current_chat.send(lines)
        if self.exiting:
            raise ExitMainLoop()

    @command
    def help(self, arg):
        """help on ja commands"""
        self.print("available commands:")
        maxlength = max(map(lambda x: len(x), self.commands.keys()))
        for name in sorted(self.commands.keys()):
            doc = self.commands[name].__doc__
            if not doc:
                doc = "no documentation available"
            else:
                doc = doc.split("\n", 1)[0]
            self.print("  {} -- {}".format(name.ljust(maxlength), doc))

    def keypress(self, key):
        if key == 'enter':
            self.execute(self.__input())
        else:
            self.print("unhandled key press {}".format(key))

    @command
    def load(self, arg):
        """load ja plugin"""
        if not arg:
            self.print("load: specify a plugin to load")
            return
        args = arg.split(' ', 1)
        modname = args[0]
        arg = args[1] if len(args) > 1 else None
        try:
            __import__(modname)
            plugin = sys.modules[modname].instance(self, arg)
            if plugin:
                name = plugin.name
                if name in self.plugins:
                    self.print("plugin {} already loaded".format(name))
                else:
                    self.plugins[name] = plugin
                    self.__setup_plugin_commands(plugin, name)
                    self.print("loaded plugin {} from {}".format(name, modname))
        except ImportError as e:
            self.print("cannot find plugin {}: {}".format(modname, e))
        except AttributeError as e:
            self.print("{} is not a ja plugin: {}".format(modname, e))

    def print(self, text, level=TWITTER):
        self.log.append((datetime.now(), level, text))
        self.__refresh_sysview()

    @command
    def quit(self, arg):
        """quit ja"""
        for c in self.connections:
            c.disconnect()
        del self.connections
        self.exiting = True

    @redraw_screen
    def receive_message(self, message):
        for chat in self.chats:
            if chat.accept_message(message):
                return
        chat = Chat(ja=self, message=message)
        chat.widget = ChatWidget(chat)
        self.chats.append(chat)
        self.print("created new window {} for chat with {}".format(len(self.chats)-1, chat.contact))

    def run(self, args):
        self.__setup_ui()
        self.__setup_commands()
        return self.loop.run()

    def select_connection(self, contact):
        pass # TODO

    @command
    @redraw_screen
    def window(self, arg):
        """switch to window with given number"""
        if arg == "system":
            self.view.set_body(self.sysview)
            self.current_chat = None
        else:
            try:
                wid = int(arg)
                self.view.set_body(self.chats[wid].widget)
                self.current_chat = self.chats[wid]
            except (ValueError, IndexError):
                self.print("{} is not a window".format(arg))

def ja(*args, **kwargs):
    if not hasattr(ja, 'instance'):
        ja.instance = Ja(*args, **kwargs)
    return ja.instance

# vim:sw=4:ts=4:et
