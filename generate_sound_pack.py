from pydub import AudioSegment
import shutil
import os
from os import mkdir
from os.path import exists, abspath, join 
import re
import json

"""Takes a folder with sound files and converts them to a resource pack (sound pack)
"""

EXPORT_FORMAT = "ogg"

SOUND_PACK_NAME = "test_pack"

META_TEMPLATE_PATH = abspath(f"./pack.mcmeta")

IN_PATH = abspath(f"./sounds")
SOUND_LIST_PATH = abspath(f"./sounds_{29}.json")
pack_path = abspath(f"./{SOUND_PACK_NAME}")
pack_assets_path = join(pack_path, "assets/minecraft/")
pack_sounds_path = join(pack_assets_path, "sounds/")
pack_sounds_json_path = join(pack_path, "sounds.json")
pack_metha_path = join(pack_path, "pack.mcmeta")

def ensure_path_exists_to(path):
    head = os.path.split(path)[0]
    if not exists(head):
        os.makedirs(head)

class Sound:
    ALPHANUM = "[a-zA-Z0-9]"
    SNAKE_WORD = f"({ALPHANUM}+_)*{ALPHANUM}+"

    ID = f"{SNAKE_WORD}"
    PATH = f"({SNAKE_WORD}-)*{SNAKE_WORD}_?"
    EXT = f"{ALPHANUM}+"

    def __init__(self, filename):
        # Check if the filename matches the 
        search_string = f"^((?P<id>{Sound.ID})__)?(?P<path>{Sound.PATH})\.(?P<ext>{Sound.EXT})$"
        match = re.search(search_string, filename)

        if not match:
            raise ValueError("File name format incorrect.")

        self.filename = filename
        self.filepath = os.path.join(IN_PATH, filename)
        self.id = match.group('id')
        self.mc_path = match.group('path')
        self.mc_path_slashes = self.mc_path.replace("-", "/")
        self.ext = match.group('ext')

    
if __name__ == "__main__":

    dir_entries = os.listdir(IN_PATH)

    sound_dict = {}

    print(f"Checking Entries in {IN_PATH}:")
    for entry in dir_entries:
        try:
            p = Sound(entry)
            if sound_dict.get(p.mc_path):
                sound_dict[p.mc_path].append(p)
            else:
                sound_dict[p.mc_path] = [p]
        except ValueError as e:
            print(f"Skipping \"{entry}\" because: {e}")

    print(f"Comparing against sound paths found in {SOUND_LIST_PATH} names:")

    with open(SOUND_LIST_PATH, 'r') as f:
        mc_sound_list = json.load(f)

    to_remove = []
    
    for p in [*sound_dict.keys()]:
        l = len(sound_dict[p])
        if p not in mc_sound_list.keys():
            print(f"Skipping \"{p}\" ({l} files) because: Not a valid path to a minecaft sound.")
            sound_dict.pop(p)
            continue
        elif l > mc_sound_list[p]:
            l2 = mc_sound_list[p]
            print(f"Skipping the last {l - l2} files for \"{p}\" ({l} files), since there are only {l2} variants in minecraft.")
            sound_dict[p] = sound_dict[p][:l2]

    print(f"Converting and saving sounds:")

    for k, sounds in sound_dict.items():
        for i, s in enumerate(sounds):
            export_path = os.path.join(pack_sounds_path, f"{s.mc_path_slashes}{'' if mc_sound_list[k] == 1 else i+1}.{EXPORT_FORMAT}")
            try:
                seg = AudioSegment.from_file(s.filepath)
            except Exception as e:
                print(f"Skipping {s.filepath}, could not read in file: {e}")
                continue
            ensure_path_exists_to(export_path)
                
            seg.export(export_path, format=EXPORT_FORMAT)
    # add pack.mcmeta
    ensure_path_exists_to(pack_metha_path)
    shutil.copyfile(META_TEMPLATE_PATH, pack_metha_path)
