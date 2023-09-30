import re
import sys
from pathlib import Path
import shutil

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")


TRANS = {}

images_files = list()
documents_files = list()
video_files = list()
music_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()
#images = ("JPEG", "PNG", "JPG", "SVG", "imit")
# не можу зрозуміти, як правильно замінити ключі з однаковим значенням на кортеж
# та пройтись по даному кортежу ключів в словнику, щоб не розписувати кожен окремо
registered_extensions = {
    #images[slice(-1)]: images_files,
    "JPEG": images_files,
    "PNG": images_files,
    "JPG": images_files,
    "SVG": images_files,
    "TXT": documents_files,
    "DOCX": documents_files,
    "DOC": documents_files,
    "PDF": documents_files,
    "XLSX": documents_files,
    "PPTX": documents_files,
    "AVI": video_files,
    "MP4": video_files,
    "MOV": video_files,
    "MKV": video_files,
    "MP3": music_files,
    "OGG": music_files,
    "WAV": music_files,
    "AMR": music_files,
    "ZIP": archives,
    "GZ": archives,
    "TAR": archives
}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("images", "documents", "video", "audio", "archives"):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)

def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize(path.name))


def move_archive(archieve, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)

    name = normalize(archieve.name.rsplit(".", 1)[0])
    archieve_folder = target_folder/name
    archieve_folder.mkdir(exist_ok=True)
    try:    
        shutil.unpack_archive(str(archieve.resolve()), str(archieve_folder.resolve()))
    except shutil.ReadError:
        archieve_folder.rmdir()
        return
    except FileNotFoundError:
        archieve_folder.rmdir()
        return
    archieve.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass

def main():
    path = sys.argv[1]
    print(f"Start in {path}")
    folder_path = Path(path)

    scan(folder_path)

    for file in images_files:
        hande_file(file, folder_path, "images")

    for file in documents_files:
        hande_file(file, folder_path, "documents")

    for file in video_files:
        hande_file(file, folder_path, "video")

    for file in music_files:
        hande_file(file, folder_path, "audio")

    for file in archives:
        move_archive(file, folder_path, "archives")

    get_folder_objects(folder_path)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Not enough parameters")
        quit()
    path = sys.argv[1]
    print(f"Start in {path}")
    arg = Path(path)
    main(arg.resolve())

