"""
Holds all the classes for neoforge modding
"""
import io
import os
import subprocess
import urllib.request
import urllib.error
import zipfile
from pathlib import Path

from ._utils import find_and_replace
from .shared import ModConfig

class NeoforgeMod:
    """Main mod class for neoforge mods"""

    def __init__(self, config: ModConfig) -> None:
        self.config = config
        self.mod_folder_name = f"{config.mod_id}-modfiles"
        group_id_to_folder = str(self.config.mod_group_id).replace(".", "/")
        self.mod_java_folder = f"{self.mod_folder_name}/src/main/java/{group_id_to_folder}"

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
                original_root_folder = zip_ref.namelist()[0].split('/')[0]
                zip_ref.extractall(destination_path)

            old_folder_path = os.path.join(destination_path, original_root_folder)
            new_folder_path = os.path.join(destination_path, self.mod_folder_name)

            os.rename(old_folder_path, new_folder_path)

            print("Mod files successfully extracted")
        except urllib.error.HTTPError as e:
            print(f"An HTTP error occurred: {e.code}. Try running again")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def _fill_gradle_props(self) -> None:
        """Fill the default gradle.properties file with correct content"""
        properties = self.config.gen_neo_gradle_prop()
        gradle_props_file = Path(f"{self.mod_folder_name}/gradle.properties")
        gradle_props_file.write_text(properties)

    def _replace_neoforge_mods_toml(self) -> None:
        """Replace default values in neoforge.mods.tol with updated contents from config object"""
        mod_toml_path = f"{self.mod_folder_name}/src/main/templates/META-INF/neoforge.mods.toml"
        if self.config.mod_homepage_url is not None:
            find_and_replace('#displayURL="https://change.me.to.your.mods.homepage.example.invalid/" #optional', f'displayURL="{self.config.mod_homepage_url}"', mod_toml_path)
        if self.config.mod_logo_file is not None:
            find_and_replace('#logoFile="examplemod.png" #optional', f'logoFile="{self.config.mod_logo_file}"', mod_toml_path)
        if self.config.mod_credits is not None:
            find_and_replace('#credits="" #optional', f'credits="{self.config.mod_credits}"', mod_toml_path)
        if self.config.mod_authors is not None:
            find_and_replace('#authors=""', f'authors="{self.config.mod_authors}"', mod_toml_path)
        if self.config.mod_description is not None:
            find_and_replace("""description='''
Example mod description.
'''""", f"""description='''
{self.config.mod_description}
'''""", mod_toml_path)

    def run_neoforge_client(self) -> None:
        """Starts the Neoforge client using gradle. Also checks if the mod files are found and fills the gradle.properties and neoforge.mods.toml"""

        # Check if the mod folder exists, if not clone the directory
        if not Path(self.mod_folder_name).is_dir():
            self._clone_neoforge_repo(".")

        # fill the gradle.properties and neoforge.mods.toml
        self._fill_gradle_props()
        self._replace_neoforge_mods_toml()

        gradle_exe = 'gradlew.bat' if os.name == 'nt' else './gradlew'
        gradle_command = [gradle_exe, 'runClient']

        print("Launching the NeoForge client")

        try:
            is_windows = os.name == 'nt'
            subprocess.run(gradle_command, cwd=self.mod_folder_name, shell=is_windows, check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while trying to start the NeoForge client: {e}")
        except FileNotFoundError:
            print("The gradle exe was not found, try deleting the mod folder and running again.")