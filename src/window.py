# window.py
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

from gi.repository import Adw, Gtk


@Gtk.Template(resource_path="/org/vanillaos/Sideloader/gtk/window.ui")
class SideloaderWindow(Adw.ApplicationWindow):
    __gtype_name__ = "SideloaderWindow"

    bin_main = Gtk.Template.Child()

    install_status_page = Gtk.Template.Child()
    done_status_page_install = Gtk.Template.Child()

    uninstall_status_page = Gtk.Template.Child()
    done_status_page_uninstall = Gtk.Template.Child()

    loading_status_page = Gtk.Template.Child()
    progress_bar = Gtk.Template.Child()

    def __init__(self, app_name, app_icon=None, **kwargs):
        super().__init__(**kwargs)

        self.install_status_page.set_title(_("Install {}?").format(f'"{app_name}"'))
        self.uninstall_status_page.set_title(_("Uninstall {}?").format(app_name))

        if app_icon:
            self.install_status_page.set_paintable(app_icon.get_paintable())
        else:
            self.install_status_page.set_icon_name("package-x-generic-symbolic")
