# main.py
#
# Copyright 2023 Vanilla OS Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi
import logging
from gettext import gettext as _

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Vte", "3.91")

from gi.repository import Gtk, GLib, Gio, Adw
from vanilla_sideload.window import SideloaderWindow
from vanilla_sideload.backend.types import ValidSideloadAction


logging.basicConfig(level=logging.INFO)


class SideloadApplication(Adw.Application):
    """The main application singleton class."""

    __requested_action: ValidSideloadAction
    __package_path: str

    def __init__(self):
        super().__init__(
            application_id="org.vanillaos.Sideload",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        self.create_action("quit", self.quit, ["<primary>q"])

        self.__register_arguments()

    def __register_arguments(self):
        """Register command line arguments."""
        self.add_main_option(
            "install",
            ord("i"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            "Install a package",
            None,
        )
        self.add_main_option(
            "uninstall",
            ord("u"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            "Uninstall a package",
            None,
        )

    def do_command_line(self, command):
        """Handle command line arguments.

        We only have one command line option, --embedded, which
        indicates that the application is embedded in another
        application.
        """

        commands = command.get_options_dict()

        install_option = commands.lookup_value("install")
        uninstall_option = commands.lookup_value("uninstall")

        if install_option:
            self.__requested_action = ValidSideloadAction.INSTALL
            self.__package_path = install_option.get_string()
        elif uninstall_option:
            self.__requested_action = ValidSideloadAction.UNINSTALL
            self.__package_path = uninstall_option.get_string()
        else:
            print("No action specified")
            return 0

        return self.do_activate()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = SideloaderWindow(
                pkg_path=self.__package_path,
                requested_action=self.__requested_action,
                application=self,
            )
        win.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = SideloadApplication()
    return app.run(sys.argv)
