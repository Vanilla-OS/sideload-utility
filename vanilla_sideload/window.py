# window.py
#
# Copyright 2024 Vanilla OS Contributors
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

from gettext import gettext as _
from gi.repository import Adw, Gtk
from typing import Text, Dict, Any, Callable, Optional

from vanilla_sideload.backend.dpkg import DpkgResolver
from vanilla_sideload.backend.android import AndroidResolver
from vanilla_sideload.backend.types import ValidSideloadAction, DebPackage
from vanilla_sideload.views.install_done import SideloaderInstallDone
from vanilla_sideload.views.install import SideloaderInstall
from vanilla_sideload.views.loading import SideloaderLoading
from vanilla_sideload.views.uninstall_done import SideloaderUninstallDone
from vanilla_sideload.views.uninstall import SideloaderUninstall


@Gtk.Template(resource_path="/org/vanillaos/Sideload/gtk/window.ui")
class SideloaderWindow(Adw.ApplicationWindow):
    __gtype_name__: Text = "SideloaderWindow"

    bin_main: Adw.Bin = Gtk.Template.Child()

    __pkg: Optional[DebPackage] = None

    def __init__(
        self,
        pkg_path: Text,
        requested_action: ValidSideloadAction,
        **kwargs: Dict[str, Any],
    ) -> None:
        super().__init__(**kwargs)
        self.__pkg_path: Text = pkg_path
        self.__requested_action: ValidSideloadAction = requested_action
        self.__aresolver: AndroidResolver = AndroidResolver(pkg_path)
        self.__dresolver: DpkgResolver = DpkgResolver(pkg_path)

        self.__build_ui()

    def __build_ui(self) -> None:
        def callback(result: Any, error: Optional[Exception]) -> None:
            # TODO: handle result
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

        async_func: Callable[[], Any]
        if self.__requested_action == ValidSideloadAction.INSTALL:
            async_func = self.__read_package_info
        elif self.__requested_action == ValidSideloadAction.UNINSTALL:
            async_func = self.__read_installed_package_info
        else:
            raise ValueError("Invalid action requested")

        view_loading = SideloaderLoading(
            _("Reading package information"),
            _("This may take a while..."),
            async_func,
        )
        view_loading.connect("done", callback)

        self.bin_main.set_child(view_loading)

    def __build_install_ui(self) -> None:
        self.view_install = SideloaderInstall(self, self.__pkg)
        self.view_install.connect("done", self.__on_install_done)
        self.bin_main.set_child(self.view_install)

    def __on_install_done(self, view_install: SideloaderInstall, *args: Any) -> None:
        success = not bool(args[0])
        view_install_done = SideloaderInstallDone(self.__pkg.name)
        view_install_done.btn_logs.connect("clicked", self.__on_view_logs)
        if not success:
            view_install_done.status.set_title(_("Installation Failed"))
            view_install_done.status.set_description(_("The package installation was unsuccessful"))
            view_install_done.status.set_property("icon-name", "dialog-error-symbolic")
        self.bin_main.set_child(view_install_done)

    def __build_uninstall_ui(self) -> None:
        view_uninstall = SideloaderUninstall(self.__pkg)
        self.bin_main.set_child(view_uninstall)

    def __read_package_info(self) -> None:
        if self.__pkg_path.endswith(".apk"):
            self.__pkg = self.__aresolver.extract_info()
        elif self.__pkg_path.endswith(".deb"):
            self.__pkg = self.__dresolver.extract_info()

        if not self.__pkg:
            raise ValueError("Unable to extract package information")

    def __read_installed_package_info(self) -> None:
        raise NotImplementedError("Not implemented yet")

    def __on_view_logs(self, *args):
        self.view_install.btn_console.set_visible(False)
        self.view_install.progress_bar.set_visible(False)
        self.view_install.btn_quit.set_visible(True)
        self.view_install.box_console_main.show()
        self.bin_main.set_child(self.view_install)
