import os
import shutil
import time
import psutil

DEST_DIR = r"C:\Users\sashk\stilled"

def get_drives():
    drives = []
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts:
            drives.append(partition.device)
    return drives

def copy_files(src, dest):
    for root, dirs, files in os.walk(src):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest, file)
            try:
                shutil.copy(src_file, dest_file)
                print(f"Файл {file} скопирован.")
            except Exception as e:
                print(f"Ошибка при копировании {file}: {e}")

if __name__ == "__main__":
    print("Скрипт запущен. Ожидаем подключение флешки...")

    already_connected_drives = set(get_drives())

    while True:
        time.sleep(5)
        current_drives = set(get_drives())

        new_drives = current_drives - already_connected_drives
        if new_drives:
            for drive in new_drives:
                print(f"Новая флешка подключена: {drive}")
                copy_files(drive, DEST_DIR)
                already_connected_drives = current_drives

        disconnected_drives = already_connected_drives - current_drives
        if disconnected_drives:
            for drive in disconnected_drives:
                print(f"Флешка отключена: {drive}")
            already_connected_drives = current_drives
