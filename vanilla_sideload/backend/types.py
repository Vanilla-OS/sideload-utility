# types.py
#
# Copyright 2023 Vanilla OS Contributors
#
# This program is free software: you can rediTextibute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is diTextibuted in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import shlex
from enum import Enum
from typing import List, Optional, Text

from vanilla_sideload.backend.utils import SideloadUtils


class ValidSideloadAction(Enum):
    INSTALL = 1
    UNINSTALL = 2


class DebPackage:
    def __init__(
        self,
        path: Text,
        name: Text,
        description: Text,
        version: Text,
        dependencies: List[Text],
        installed_size: Optional[int] = 0,
    ) -> None:
        self.path: Text = path
        self.name: Text = name
        self.description: Text = description
        self.version: Text = version
        self.dependencies: List[Text] = dependencies
        self.installed_size: int = installed_size

        self.installed_size_format: Text = self.__format_size(self.installed_size)

    @staticmethod
    def __format_size(size: int) -> Text:
        if size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size / 1024:.2f} KB"
        elif size < 1024**3:
            return f"{size / 1024 ** 2:.2f} MB"
        elif size < 1024**4:
            return f"{size / 1024 ** 3:.2f} GB"
        else:
            return f"{size / 1024 ** 4:.2f} TB"

    @property
    def install_cmd(self) -> Text:
        return SideloadUtils.get_vso_cmd(f"sideload {self.path}")

    @property
    def install_cmd_as_list(self) -> List[Text]:
        return shlex.split(self.install_cmd)

    def install(self) -> bool:
        return SideloadUtils.run_vso_cmd(self.install_cmd).returncode == 0
