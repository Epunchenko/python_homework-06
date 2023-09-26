import shutil
import sys
import scan
import normalize
from pathlib import Path



def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))


def move_archive(archieve, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)

    name = normalize.normalize(archieve.name.rsplit(".", 1)[0])
    archieve_folder = target_folder/name
    archieve_folder.mkdir(exist_ok=True)
    try:    
        shutil.unpack_archive(archieve, archieve_folder/name)
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

def main(folder_path):
    scan.scan(folder_path)

    for file in scan.images_files:
        hande_file(file, folder_path, "images")

    for file in scan.documents_files:
        hande_file(file, folder_path, "documents")

    for file in scan.video_files:
        hande_file(file, folder_path, "video")

    for file in scan.music_files:
        hande_file(file, folder_path, "audio")

    for file in scan.archives:
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
