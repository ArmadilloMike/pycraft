"""
Holds all the classes for neoforge modding
"""
import io
import urllib.request
import urllib.error
import zipfile

from .shared import ModConfig

class NeoforgeMod:
    """Main mod class for neoforge mods"""
    config: ModConfig

    def _clone_neoforge_repo(self, destination_path: str) -> None:
        """Clones the neoforge repo for the version of minecraft"""
        if self.config.minecraft_version == "1.21.1":
            git_url = "https://github.com/NeoForgeMDKs/MDK-1.21.1-ModDevGradle".rstrip("/")
        elif self.config.minecraft_version == "26.1":
            git_url = "https://github.com/NeoForgeMDKs/MDK-26.1-ModDevGradle".rstrip("/")
        else:
            git_url = "https://github.com/NeoForgeMDKs/MDK-1.21.1-ModDevGradle".rstrip("/")
        zip_url = f"{git_url}/archive/refs/heads/main.zip"

        try:
            print("Downloading mod files, please be patient")

            with urllib.request.urlopen(zip_url) as response:
                zip_buffer = io.BytesIO(response.read())

            print("Extracting mod files, please be patient")
            with zipfile.ZipFile(zip_buffer) as zip_ref:
                zip_ref.extractall(destination_path)

            print("Mod files successfully extracted")
        except urllib.error.HTTPError as e:
            print(f"An HTTP error occurred: {e.code}. Try running again")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")