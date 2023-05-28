# main.py
#
# Copyright 2023 kramo
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
from pathlib import Path
from time import sleep

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

# pylint: disable=wrong-import-order, wrong-import-position
from gi.repository import Adw, Gio, GLib, Gtk

from .window import SideloaderWindow


class SideloaderApplication(Adw.Application):
    """The main application singleton class."""

    win = None

    def __init__(self):
        super().__init__(
            application_id="org.vanillaos.Sideloader",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action(
            "close_window",
            lambda *_: self.props.active_window.close(),  # pylint: disable=no-member
            ["<primary>w", "Escape"],
        )
        self.create_action("install", self.on_install_action)
        self.create_action("uninstall", self.on_uninstall_action)
        self.create_action("open", self.on_open_action)

        # Set these from the CLI
        self.app_name = "App Name"
        self.app_icon = None
        self.path = Path("/test/path/to/app.apk")
        self.action = "uninstall"

        if self.action == "install":
            self.app_name = self.path.name
            self.app_icon = self.create_icon()

    def do_activate(self):  # pylint: disable=arguments-differ
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """

        self.win = self.props.active_window  # pylint: disable=no-member
        if not self.win:
            self.win = SideloaderWindow(self.app_name, self.app_icon, application=self)

        self.win.bin_main.set_child(
            self.win.install_status_page
            if self.action == "install"
            else self.win.uninstall_status_page
        )

        self.win.present()

    def on_open_action(self, *_args):
        pass  # Command for VSO to open the app

    def create_icon(self):
        # Extract the icon from the .apk/.deb file here
        return Gtk.Image.new()

    def pulse_progress_bar(self):
        def pulse():
            while True:
                sleep(0.1)
                self.win.progress_bar.pulse()

        GLib.Thread.new(None, pulse)

    def show_done(self, _pid, _wait_status):
        if self.action == "install":
            self.win.done_status_page_install.set_title(
                _("{} Successfully installed.").format(f'"{self.app_name}"')
            )

            self.win.bin_main.set_child(self.win.done_status_page_install)

        elif self.action == "uninstall":
            self.win.done_status_page_uninstall.set_title(
                _("{} Successfully uninstalled.").format(self.app_name)
            )

            self.win.bin_main.set_child(self.win.done_status_page_uninstall)

    def on_install_action(self, *_args):
        self.win.loading_status_page.set_title(
            _("Installing {}...").format(f'"{self.app_name}"')
        )

        self.win.bin_main.set_child(self.win.loading_status_page)
        self.pulse_progress_bar()

        argv = ["sleep", "3"]  # VSO command goes here

        pid = GLib.spawn_async(argv, flags=GLib.SpawnFlags.SEARCH_PATH)[0]

        GLib.child_watch_add(GLib.PRIORITY_DEFAULT, pid, self.show_done)

    def on_uninstall_action(self, *_args):
        self.win.loading_status_page.set_title(
            _("Uninstalling {}...").format(self.app_name)
        )

        self.win.bin_main.set_child(self.win.loading_status_page)
        self.pulse_progress_bar()

        argv = ["sleep", "3"]  # VSO command goes here

        pid = GLib.spawn_async(argv, flags=GLib.SpawnFlags.SEARCH_PATH)[0]

        GLib.child_watch_add(GLib.PRIORITY_DEFAULT, pid, self.show_done)

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


def main(version):  # pylint: disable=unused-argument
    """The application's entry point."""
    app = SideloaderApplication()
    return app.run(sys.argv)
