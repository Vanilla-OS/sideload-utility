# utils.py
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

from typing import Optional, Text
import os
import shutil
import subprocess


class SideloadUtils:
    @staticmethod
    def get_vso_cmd(command: Text) -> Text:
        if os.path.exists("/run/.containerenv"):
            vso_bin: Optional[Text] = f"{shutil.which('host-spawn')} vso"
        else:
            vso_bin: Optional[Text] = shutil.which("vso")

        return f"{vso_bin} {command}"

    @staticmethod
    def run_vso_cmd(command: Text) -> subprocess.CompletedProcess:
        proc = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = proc.communicate()
        return subprocess.CompletedProcess(
            args=command,
            returncode=proc.returncode,
            stdout=stdout.decode(),
            stderr=stderr.decode(),
        )
