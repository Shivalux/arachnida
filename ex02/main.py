import sys
import os
from datetime import datetime
from exif import Image, Flash
from pathlib import Path

IMG_TYPE = { ".jpg", ".jpeg", ".png", ".gif", ".bmp" }
FLASH_ATTR = { "flash_fired", "flash_mode", "flash_return", "flash_function_not_presen", "red_eye_reduction_supported", "reserved" }
USAGE = '''\
------------------------------------------------------------------------------------------------------------------------
USAGE: ./scorpion FILE1 [FILE2 ...]
------------------------------------------------------------------------------------------------------------------------
Option: 
 • -m        : modify/delete the metadata of a given file as parameter.
------------------------------------------------------------------------------------------------------------------------
Supporting the following extensions by default:  [ .jpg / .jpeg / .png / .gif / .bmp ]
------------------------------------------------------------------------------------------------------------------------
'''
def main() -> int:
    if len(sys.argv) <= 1:
        print(USAGE)
        return 1
    if sys.argv[1] == '-m':
        if len(sys.argv <= 3):
            return error("Invalid argument. need file path.", 1)
        modify_data(Path(path), os.stat(path))
    else:
        for i, path in enumerate(sys.argv[1:]):
            print_data(Path(path), os.stat(path), i + 1)
    return 0

def print_data(path, stats, count: int=0):
    try:
        print(f"{'-' * 69}")
        print(f"IMAGE-[{count:03d}]::[{os.path.abspath(path)}]")
        print(f"|{'=' * 29}METADATA]{'=' * 30}|")
        print(f"| File Name:        {path.name}".ljust(68), "|")
        print(f"| File Type:        {path.suffix.upper().strip('.')} image".ljust(68), "|")
        print(f"| Size (KB):        {stats.st_size / 1024:.2f} KB".ljust(68), "|")
        print(f"| Creation Date:    {time(stats.st_ctime)}".ljust(68), "|")
        print(f"| Modified Date:    {time(stats.st_mtime)}".ljust(68), "|")
        print(f"| Last Access Date: {time(stats.st_atime)}".ljust(68), "|")
        print(f"|{'=' * 30}[EXIF]{'=' * 32}|")
        with open(path, 'rb') as image_file:
            my_image = Image(image_file)
        if my_image.has_exif:
            for i in my_image.list_all():
                key = i.replace("_", " ").strip().title()
                if (key == 'Copyright'): continue
                try:
                    if isinstance(my_image[i], Flash):
                        print(f"| • {key}:".ljust(68), "|")
                        for attr in dir(my_image[i]):
                            if attr in FLASH_ATTR:
                                print(f"| |- • {attr}: {getattr(my_image[i], attr)}".ljust(68), "|")
                    else:
                        print(f"| • {key}: {my_image[i]}".ljust(68), "|")
                except Exception as e:
                    pass
        else:
            print(f"|{' ' * 17}This image file does not has EXIF{' ' * 18}|")
        print(f"[IMAGE]::[{count:03d}]--".rjust(70, '-'))
    except FileNotFoundError:
        return error(f"File is not found [{path}]", 1)

def modify_data():
    tag = []
    return;

def print_promt():
    return

def size(byte: int) -> int:
    return format(int(bytes)/1024, ".2f")

def time(timestamp: int) -> str:
    dt = datetime.fromtimestamp(timestamp)
    return str(dt).split('.')[0]

def error(message: str, return_code: int=None):
    print(f"[ERROR]: {message}")
    return return_code

if __name__ == "__main__":
    main()
