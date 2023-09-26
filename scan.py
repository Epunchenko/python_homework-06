import sys
from pathlib import Path


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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Not enough parameters")
        quit()
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

    print(f"images: {images_files}\n")
    print(f"documents: {documents_files}\n")
    print(f"video: {video_files}\n")
    print(f"music: {music_files}\n")
    print(f"archive: {archives}\n")
    print(f"unknown: {others}\n")
    print(f"All extensions: {extensions}\n")
    print(f"Unknown extensions: {unknown}\n")