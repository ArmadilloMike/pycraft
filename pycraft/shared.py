"""
Shared classes and functions between the different mod loaders
"""
from dataclasses import dataclass


@dataclass
class ModConfig:
    """Mod Config class for both fabric and neoforge"""
    name: str
    mod_id: str = "examplemod"
    version: str = "1.0.0"

    def to_dict(self) -> dict:
        """Turns the object into a dictionary"""
        data = {
            "name": self.name,
            "mod_id": self.mod_id,
            "version": self.version
        }