"""Internal utility functions"""
import urllib.request
import json

def find_and_replace(old_text, new_text, file_path) -> None:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    updated_content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_content)

def gen_vanilla_items() -> None:
    url = "https://raw.githubusercontent.com/PrismarineJS/minecraft-data/refs/heads/master/data/pc/1.21.4/items.json"
    print("Downloading Minecraft items list...")
    with urllib.request.urlopen(url) as response:
        items_data = json.loads(response.read().decode())
    print(f"Processing {len(items_data)} items into Python code...")
    with open("generated_items.py", "w", encoding="utf-8") as f:
        f.write('from dataclasses import dataclass\n\n')
        f.write('@dataclass\n')
        f.write('class Item:\n')
        f.write('    id: str\n')
        f.write('    display_name: str\n')
        f.write('    stack_size: int\n\n\n')
        f.write('class Items:\n')
        f.write('    """Auto-generated Minecraft Item Registry Mapping"""\n')
        for item in items_data:
            clean_name = item['name'].upper()
            if clean_name[0].isdigit():
                clean_name = f"ITEM_{clean_name}"
            id_str = f"minecraft:{item['name']}"
            display_name = item.get('displayName', item['name'].replace('_', ' ').title())
            stack_size = item.get('stackSize', 64)
            f.write(f'    {clean_name} = Item("{id_str}", "{display_name}", {stack_size})\n')
    print("Successfully written to generated_items.py!")