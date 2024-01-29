# utils.py
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

from typing import Text
import os
import shutil
import subprocess


class SideloadUtils:
    @staticmethod
    def get_vso_cmd(command: Text) -> Text:
        vso_bin: Text = "vso"
        use_host_spawn: bool = False

        if os.path.exists("/run/.containerenv"):
            use_host_spawn = True
        
        if os.path.exists(f"{os.environ['VSO_PATH']}/vso"):
            vso_bin = f"{os.environ['VSO_PATH']}/vso"

        elif os.path.exists(f"{os.getcwd()}/vso"):
            vso_bin = f"{os.getcwd()}/vso"

        elif vso_bin is None:
            vso_bin = shutil.which("vso")

        return (
            f"{shutil.which('host-spawn')} {vso_bin} {command}"
            if use_host_spawn
            else f"{vso_bin} {command}"
        )

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
