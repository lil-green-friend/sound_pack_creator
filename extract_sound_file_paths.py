import sys
import json
import os

""" Converts a minecraft assets index to a list of sound file paths in json format"""

if __name__ == "__main__":
    filepath = sys.argv[1]
    assert filepath is not None and os.path.exists(filepath), "Provide a valid filepath to the index"
    filename = os.path.basename(filepath)
    
    with open(filepath, 'r') as file:
        data = json.load(file)
        filepaths = list(data["objects"].keys())
        sound_paths = [path.replace("minecraft/sounds/", "").replace(".ogg", "").replace("/", '-') for path in filepaths if path.startswith("minecraft/sounds/")]
        print(f"Found {len(sound_paths)} sounds")

        sound_dict = {}
        for path in sound_paths:
            base_path = path.rstrip('0123456789')
            if base_path[-1] == "/": # special case where entire file name is a number (e.g. for records 5, 11, and 13)
                base_path = path
            sound_dict[base_path] = sound_dict.get(base_path, 0) + 1
        sound_paths = sound_dict

        
        output_filename = f"sounds_{filename}"
        with open(output_filename, 'w') as f:
            json.dump(sound_paths, f, indent=4)
            print(f"Wrote paths to {output_filename}")


