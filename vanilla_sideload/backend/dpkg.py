import os
import subprocess
import tempfile
import shutil
from typing import List, Optional, Text


class DebPackage:
    def __init__(
        self,
        name: Text,
        description: Text,
        version: Text,
        dependencies: List[Text],
        icon_path: Optional[Text],
    ):
        self.name = name
        self.description = description
        self.version = version
        self.dependencies = dependencies
        self.icon_path = icon_path


class DpkgResolver:
    def __init__(self, package_path: Text):
        self.package_path = package_path
        self.__dpkg = self.__get_dpkg_args()

    def __get_dpkg_args(self) -> List[Text]:
        args = ["vso", "run", "dpkg-deb"]
        if shutil.which("host-spawn") is not None:
            args = ["host-spawn"] + args
        return args

    def extract_info(self) -> Optional[DebPackage]:
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                subprocess.check_output(
                    self.__dpkg + ["-x", self.package_path, tmp_dir]
                )
                icon_files = [f for f in os.listdir(tmp_dir) if f.endswith(".png")]
                icon_path = None
                if icon_files:
                    icon_filename = icon_files[0]
                    icon_path = os.path.join(tmp_dir, icon_filename)
        except subprocess.CalledProcessError as e:
            print(f"Error: Unable to extract package icon. {e}")
            icon_path = None
        except FileNotFoundError as e:
            print(f"Error: {e}")
            icon_path = None

        info = self.extract_package_info()
        if not info:
            return None

        name = self.extract_field(info, "Package")
        description = self.extract_field(info, "Description")
        version = self.extract_field(info, "Version")
        dependencies = self.extract_dependencies(info)

        return DebPackage(name, description, version, dependencies, icon_path)

    def extract_package_info(self) -> Optional[Text]:
        try:
            info = subprocess.check_output(self.__dpkg + ["-I", self.package_path])
            info = info.decode("utf-8")
            return info
        except subprocess.CalledProcessError as e:
            print(f"Error: Unable to extract package information. {e}")
            return None

    def extract_field(self, info: Text, field_name: Text) -> Optional[Text]:
        field_start = info.find(field_name + ":")
        if field_start != -1:
            field_end = info.find("\n", field_start)
            if field_end != -1:
                field_value = info[
                    field_start + len(field_name) + 1 : field_end
                ].strip()
                return field_value
        return None

    def extract_dependencies(self, info: Text) -> List[Text]:
        dependencies_start = info.find("Depends:")
        if dependencies_start != -1:
            dependencies_end = info.find("\n", dependencies_start)
            if dependencies_end != -1:
                dependencies_value = info[
                    dependencies_start + 8 : dependencies_end
                ].strip()
                return dependencies_value.split(", ")
        return []
