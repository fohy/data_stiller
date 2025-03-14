import os
import shutil
import time
import psutil
import requests
import re

DEST_DIR = r"C:\" #Меняй на папку, куда копируешь файлы
FILE_URL = "https://avatars.mds.yandex.net/i?id=4b41399d0fe97578763ddab4b304539a_l-4589529-images-thumbs&n=13"


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
                print(f"Файл {file} скопирован из флешки в {dest}.")
            except Exception as e:
                print(f"Ошибка при копировании {file}: {e}")


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def download_file(url, dest):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = "image.png"
        file_path = os.path.join(dest, filename)

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Файл {filename} успешно загружен на флешку {dest}.")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании файла: {e}")


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
                download_file(FILE_URL, drive)
                already_connected_drives = current_drives

        disconnected_drives = already_connected_drives - current_drives
        if disconnected_drives:
            for drive in disconnected_drives:
                print(f"Флешка отключена: {drive}")
            already_connected_drives = current_drives
