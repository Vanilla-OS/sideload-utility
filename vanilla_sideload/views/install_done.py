# install_done.py
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
from typing import Text


@Gtk.Template(resource_path="/org/vanillaos/Sideload/gtk/view-install-done.ui")
class SideloaderInstallDone(Adw.Bin):
    __gtype_name__ = "SideloaderInstallDone"

    status = Gtk.Template.Child()

    def __init__(self, package_name: Text, **kwargs):
        super().__init__(**kwargs)

        self.status.set_description(
            _("Package {package_name} installed successfully").format(
                package_name=package_name
            )
        )
