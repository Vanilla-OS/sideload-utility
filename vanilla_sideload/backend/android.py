# android.py
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

from typing import List, Optional, Text
from pyaxmlparser import APK

from vanilla_sideload.backend.types import AndroidPackage


class AndroidResolver:
    def __init__(self, package_path: Text) -> None:
        self.package_path: Text = package_path

    def extract_info(self) -> Optional[AndroidPackage]:
        apk = APK(self.package_path)

        if not apk.is_valid_APK():
            return None

        name: Text = apk.get_app_name()
        description: Text = apk.package
        version: Text = apk.version_name
        dependencies: List[Text] = []
        installed_size: int = 0

        return AndroidPackage(
            path=self.package_path,
            name=name,
            description=description,
            version=version,
            dependencies=dependencies,
            installed_size=installed_size,
        )
