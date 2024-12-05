# install.py
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
from gi.repository import Adw, Gtk, Gdk, GLib, Gio, GObject, Vte, Pango
from typing import Text, Dict, Any, Tuple, List

from vanilla_sideload.backend.types import ValidSideloadAction, DebPackage


@Gtk.Template(resource_path="/org/vanillaos/Sideload/gtk/view-install.ui")
class SideloaderInstall(Adw.Bin):
    # TODO: this and the uninstall view could be merged into one view
    __gtype_name__: Text = "SideloaderInstall"
    __gsignals__: Dict[Text, Tuple[GObject.SignalFlags, Any, Tuple[bool]]] = {
        "done": (GObject.SignalFlags.RUN_FIRST, None, (bool,))
    }

    stack_main: Adw.ViewStack = Gtk.Template.Child()
    status_details: Adw.StatusPage = Gtk.Template.Child()
    status_installing: Adw.StatusPage = Gtk.Template.Child()
    btn_install: Gtk.Button = Gtk.Template.Child()
    img_install_size: Gtk.Image = Gtk.Template.Child()
    label_install_size: Gtk.Label = Gtk.Template.Child()
    progress_bar: Gtk.ProgressBar = Gtk.Template.Child()
    box_console_main: Gtk.Box = Gtk.Template.Child()
    box_console: Gtk.Box = Gtk.Template.Child()
    btn_console: Gtk.Button = Gtk.Template.Child()
    btn_quit: Gtk.Button = Gtk.Template.Child()

    __pkg: DebPackage
    __console: Vte.Terminal
    __font: Pango.FontDescription
    __fg: Gdk.RGBA
    __bg: Gdk.RGBA
    __colors: List[Gdk.RGBA]

    def __init__(self, window: Adw.ApplicationWindow, pkg: DebPackage, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.__window = window
        self.__pkg = pkg
        self.__build_ui()

    def __build_ui(self) -> None:
        self.__console = Vte.Terminal()
        self.__font = Pango.FontDescription()
        self.__font.set_family("Monospace")
        self.__font.set_size(13 * Pango.SCALE)
        self.__font.set_weight(Pango.Weight.NORMAL)
        self.__font.set_stretch(Pango.Stretch.NORMAL)

        self.status_details.set_title(self.__pkg.name)
        self.status_details.set_description(self.__pkg.description)
        self.label_install_size.set_text(self.__pkg.installed_size_format)
        self.__console.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.__console.set_font(self.__font)
        self.__console.set_mouse_autohide(True)
        self.box_console.append(self.__console)

        if self.__pkg.installed_size == 0:
            self.label_install_size.hide()
            self.img_install_size.hide()

        palette: List[Text] = [
            "#353535",
            "#c01c28",
            "#26a269",
            "#a2734c",
            "#12488b",
            "#a347ba",
            "#2aa1b3",
            "#cfcfcf",
            "#5d5d5d",
            "#f66151",
            "#33d17a",
            "#e9ad0c",
            "#2a7bde",
            "#c061cb",
            "#33c7de",
            "#ffffff",
        ]

        FOREGROUND: Text = palette[0]
        BACKGROUND: Text = palette[15]
        FOREGROUND_DARK: Text = palette[15]
        BACKGROUND_DARK: Text = palette[0]

        self.__fg = Gdk.RGBA()
        self.__bg = Gdk.RGBA()

        self.__colors = [Gdk.RGBA() for c in palette]
        [color.parse(s) for (color, s) in zip(self.__colors, palette)]
        desktop_schema = Gio.Settings.new("org.gnome.desktop.interface")
        if desktop_schema.get_enum("color-scheme") == 0:
            self.__fg.parse(FOREGROUND)
            self.__bg.parse(BACKGROUND)
        elif desktop_schema.get_enum("color-scheme") == 1:
            self.__fg.parse(FOREGROUND_DARK)
            self.__bg.parse(BACKGROUND_DARK)
        self.__console.set_colors(self.__fg, self.__bg, self.__colors)

        self.btn_install.connect("clicked", self.__on_install_clicked)
        self.btn_console.connect("clicked", self.__on_console_clicked)
        self.__console.connect("child-exited", self.on_vte_child_exited)

    def __on_install_clicked(self, btn: Gtk.Button) -> None:
        proceed: bool = True

        if self.__pkg.entity_type == "android":
            if self.__pkg.status == 1:
                proceed = False

                def on_response(dialog: Adw.MessageDialog, response: Text) -> None:
                    if response == "ok":
                        GLib.spawn_async(
                            ["kgx", "-e", "vso", "android", "init"],
                            flags=GLib.SpawnFlags.SEARCH_PATH,
                        )
                    dialog.destroy()

                dialog: Adw.MessageDialog = Adw.MessageDialog.new(
                    self.__window,
                    _("The Android subsystem is not initialized"),
                    _("You have to initialize the Android subsystem before installing Android packages. Do you want to initialize it now?"),
                )
                dialog.add_response("cancel", _("Cancel"))
                dialog.add_response("ok", _("Initialize"))
                dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
                dialog.connect("response", on_response)
                dialog.present()
        
        if proceed:
            self.stack_main.set_visible_child_name("installing")
            self.progress_bar.pulse()
            self.__console.spawn_sync(
                Vte.PtyFlags.DEFAULT,
                None,
                self.__pkg.install_cmd_as_list,
                [],
                GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                None,
            )

    def on_vte_child_exited(
        self, console: Vte.Terminal, status: int, *args: Any
    ) -> None:
        self.emit("done", bool(status))

    def __on_console_clicked(self, btn: Gtk.Button) -> None:
        status: bool = not self.box_console_main.get_visible()

        if status:
            self.box_console_main.show()
            btn.set_label("Hide Output")
            return

        self.box_console_main.hide()
        btn.set_label("Show Output")
