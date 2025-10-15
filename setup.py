import shutil
import os

import winreg as reg


def move_exe(source_path, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    exe_name = os.path.basename(source_path)
    target_path = os.path.join(target_dir, exe_name)
    shutil.move(source_path, target_path)
    return target_path

def add_context_menu_entry(exe_path, menu_name="Converter"):
    key_path = r"Software\Classes\*\shell\{}".format(menu_name)
    command_key_path = key_path + r"\command"

    try:
        reg.CreateKey(reg.HKEY_CURRENT_USER, key_path)
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_WRITE) as main_key:
            reg.SetValueEx(main_key, None, 0, reg.REG_SZ, menu_name)
            reg.SetValueEx(main_key, "Icon", 0, reg.REG_SZ, exe_path)

        reg.CreateKey(reg.HKEY_CURRENT_USER, command_key_path)
        with reg.OpenKey(reg.HKEY_CURRENT_USER, command_key_path, 0, reg.KEY_WRITE) as cmd_key:
            reg.SetValueEx(cmd_key, None, 0, reg.REG_SZ, f'"{exe_path}" "%1"')

        print(f"Successfully added context menu entry.")
        return True
    except Exception as e:
        print(f"Failed to add registry entry: {e}")

if __name__ == "__main__":
    if add_context_menu_entry(exe_path=r'C:\Waybacks-Tools\converter.exe', menu_name="Convert to another file type"):
        move_exe(source_path='converter.exe', target_dir=r'C:\Waybacks-Tools')

    k = input("Press Enter to exit...")
