import os
import tempfile
import shutil
import debian.debfile
from debian.arfile import ArFile

from typing import List, Optional, Text


class DebPackage:
    def __init__(
        self,
        name: Text,
        description: Text,
        version: Text,
        dependencies: List[Text],
        installed_size: Optional[int] = 0,
    ):
        self.name = name
        self.description = description
        self.version = version
        self.dependencies = dependencies
        self.installed_size = installed_size

        self.installed_size_format = self.__format_size(self.installed_size)

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


class DpkgResolver:
    def __init__(self, package_path: Text):
        self.package_path = package_path

    def extract_info(self) -> Optional[DebPackage]:
        with debian.debfile.DebFile(self.package_path) as deb_file:
            name = deb_file.debcontrol().get("Package", "")
            description = deb_file.debcontrol().get("Description", "")
            version = deb_file.debcontrol().get("Version", "")
            dependencies = deb_file.debcontrol().get("Depends", "").split(", ")
            installed_size = deb_file.debcontrol().get("Installed-Size", 0)

            installed_size = int(installed_size) if installed_size else 0

            return DebPackage(
                name=name,
                description=description,
                version=version,
                dependencies=dependencies,
                installed_size=installed_size,
            )
