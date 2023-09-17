# window.py
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

import time
from gi.repository import Adw, Gtk
from typing import Text, Dict, Any, Callable

from vanilla_sideload.backend.dpkg import DpkgResolver, DebPackage
from vanilla_sideload.backend.types import ValidSideloadAction
from vanilla_sideload.utils.run_async import RunAsync


@Gtk.Template(resource_path="/org/vanillaos/Sideload/gtk/window.ui")
class SideloaderWindow(Adw.ApplicationWindow):
    __gtype_name__ = "SideloaderWindow"

    bin_main = Gtk.Template.Child()

    status_install = Gtk.Template.Child()
    status_uninstall = Gtk.Template.Child()
    status_loading = Gtk.Template.Child()
    status_install_done = Gtk.Template.Child()
    status_uninstall_done = Gtk.Template.Child()
    status_operation_failed = Gtk.Template.Child()

    btn_install = Gtk.Template.Child()
    btn_uninstall = Gtk.Template.Child()
    btn_open = Gtk.Template.Child()

    label_install_size = Gtk.Template.Child()

    progress_bar = Gtk.Template.Child()

    __pkg: DebPackage
    __must_pulse: bool = False

    def __init__(
        self,
        pkg_path: Text,
        requested_action: ValidSideloadAction,
        **kwargs: Dict[str, Any],
    ):
        super().__init__(**kwargs)
        self.__requested_action = requested_action
        self.__resolver = DpkgResolver(pkg_path)

        self.__build_ui()

    def __build_ui(self):
        def callback(result, error):
            self.__must_pulse = False

            if self.__requested_action == ValidSideloadAction.INSTALL:
                if error:
                    self.__build_error_ui(_("Failed reading package information"))
                    return
                self.__build_install_ui()

            if self.__requested_action == ValidSideloadAction.UNINSTALL:
                if error:
                    self.__build_error_ui(_("Failed reading package information"))
                    return
                self.__build_uninstall_ui()

        self.__build_loading_ui(
            title=_("Reading package information"),
            description=_("This may take a while..."),
        )

        async_func: Callable
        if self.__requested_action == ValidSideloadAction.INSTALL:
            async_func = self.__read_package_info
        elif self.__requested_action == ValidSideloadAction.UNINSTALL:
            async_func = self.__read_installed_package_info
        else:
            raise ValueError("Invalid action requested")

        RunAsync(
            async_func,
            callback=callback,
        )

    def __build_install_ui(self):
        self.btn_install.connect("clicked", self.__on_install_clicked)

        self.status_install.set_title(self.__pkg.name)
        self.status_install.set_description(self.__pkg.description)

        self.label_install_size.set_text(self.__pkg.installed_size_format)

        self.bin_main.set_child(self.status_install)

    def __build_uninstall_ui(self):
        self.btn_uninstall.connect("clicked", self.__on_uninstall_clicked)

        self.status_uninstall.set_title(self.__pkg.name)

        self.bin_main.set_child(self.status_uninstall)

    def __on_install_clicked(self, button: Gtk.Button):
        print("Install clicked")

    def __on_uninstall_clicked(self, button: Gtk.Button):
        print("Uninstall clicked")

    def __on_open_clicked(self, button: Gtk.Button):
        print("Open clicked")

    def __build_error_ui(self, error_message: Text):
        self.status_operation_failed.set_title(error_message)
        self.bin_main.set_child(self.status_operation_failed)

    def __read_package_info(self):
        self.__pkg = self.__resolver.extract_info()
        if not self.__pkg:
            raise ValueError("Unable to extract package information")

    def __read_installed_package_info(self):
        raise NotImplementedError("Not implemented yet")

    def __build_loading_ui(self, title: Text, description: Text):
        def pulse():
            while True:
                if not self.__must_pulse:
                    break

                self.progress_bar.pulse()
                time.sleep(0.1)

        self.bin_main.set_child(self.status_loading)

        self.status_loading.set_title(title)
        self.status_loading.set_description(description)

        self.progress_bar.set_pulse_step(0.1)
        self.__must_pulse = True

        RunAsync(pulse)
