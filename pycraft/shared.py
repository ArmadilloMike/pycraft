"""
Shared classes and functions between the different mod loaders
"""
from dataclasses import dataclass


@dataclass
class ModConfig:
    """Mod Config class for both fabric and neoforge"""
    mod_name: str
    mod_id: str = mod_name.lower().replace(" ", "")
    mod_version: str = "1.0.0"
    minecraft_version: str = "1.21.1"
    mod_license: str  = "All Right Reserved"
    mod_group_id: str = f"dev.pycraft.{mod_id}"

    def to_dict(self) -> dict:
        """Turns the object into a dictionary"""
        data = {
            "name": self.mod_name,
            "mod_id": self.mod_id,
            "version": self.mod_version
        }
        return data