"""
Shared classes and functions between the different mod loaders
"""
from dataclasses import dataclass


@dataclass
class ModConfig:
    """Mod Config class for both fabric and neoforge"""
    mod_name: str
    mod_authors: str | None = None
    mod_logo_file: str | None = None
    mod_id: str | None = None
    mod_version: str = "1.0.0"
    minecraft_version: str = "1.21.1"
    mod_license: str  = "All Right Reserved"
    mod_group_id: str | None = None
    mod_homepage_url: str | None = None
    mod_credits: str | None = None
    mod_description: str | None = None

    def __post_init__(self) -> None:
        if self.mod_id is None:
            self.mod_id = self.mod_name.lower().replace(" ", "")
        if self.mod_group_id is None:
            self.mod_group_id = f"dev.pycraft.{self.mod_id}"
    # Version config for each version, this is the part above the mod properties in the gradle.properties
    VERSION_CONFIG = {
        "1.21.1": {
            "parchment_minecraft_version": "1.21.1",
            "parchment_mappings_version": "2024.11.17",
            "minecraft_version": "1.21.1",
            "minecraft_version_range": "[1.21.1]",
            "neo_version": "21.1.265",
            "loader_version_range": "[1,)"
        },
        "26.1": {
            "minecraft_version": "26.1",
            "minecraft_version_range": "[26.1]",
            "neo_version": "26.1.0.19-beta"
        }
    }

    def to_dict(self) -> dict:
        """Turns the object into a dictionary"""
        data = {
            "name": self.mod_name,
            "mod_id": self.mod_id,
            "version": self.mod_version
        }
        return data

    def gen_neo_grade_prop(self) -> str:
        """Generate a neoforge gradle.properties file based upon the config values set"""
        config = self.VERSION_CONFIG.get(self.minecraft_version)
        if not config:
            return ""

        properties = {
            "org.gradle.jvmargs": "-Xmx1G",
            "org.gradle.daemon": "true",
            "org.gradle.parallel": "true",
            "org.gradle.caching": "true",
            "org.gradle.configuration-cache": "true",
            **config,
            "mod_id": self.mod_id,
            "mod_name": self.mod_name,
            "mod_license": self.mod_license,
            "mod_version": self.mod_version,
            "mod>group_id": self.mod_group_id
        }

        return "\n".join(f"{k}={v}" for k, v in properties.items()) + "\n"