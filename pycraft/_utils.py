"""Internal utility functions"""

def find_and_replace(old_text, new_text, file_path) -> None:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    updated_content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_content)