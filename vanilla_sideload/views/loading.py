# loading.py
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
from gi.repository import Adw, Gtk, GObject
from typing import Text, Callable, Optional

from vanilla_sideload.backend.run_async import RunAsync


@Gtk.Template(resource_path="/org/vanillaos/Sideload/gtk/view-loading.ui")
class SideloaderLoading(Adw.Bin):
    __gtype_name__: Text = "SideloaderLoading"
    __gsignals__: dict = {
        "done": (GObject.SignalFlags.RUN_FIRST, None, (bool,)),
    }
    __func: Optional[Callable[[], None]] = None

    status: Gtk.Label = Gtk.Template.Child()
    progress_bar: Gtk.ProgressBar = Gtk.Template.Child()

    def __init__(
        self,
        title: Text,
        description: Text,
        func: Optional[Callable[[], None]] = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.__func = func

        # TODO: investigate title and description not showing up
        self.status.set_title(title)
        self.status.set_description(description)
        self.progress_bar.set_text(description)

        self.__start()

    def __start(self) -> None:
        self.progress_bar.pulse()
        RunAsync(self.__func, self.__on_done)

    def __on_done(self, result: bool, *args: object) -> None:
        self.emit("done", result)
