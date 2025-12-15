

# How to use:
- `extract_sound_file_paths.py`:
    - nimmt einen Assets-Index-Datei von Minecraft und liest nur die Sound-Pfade aus
    - ein Pfad zur Index-Datei wird als erster Commandline-Parameter übergeben 
    - das Script speichert die Pfade in einer Datei `sounds_<original_filename>.json` ab
    - die datei enthält die verschiednen Pfade, sowie die Anzahl an Varianten, die für jeden Pfad verfügbar sind
    - die Index-Dateien sind im `.minecraft`-Ordner einer Minecraft-Installation zu finden, unter `.minecraft/assets/indexes/<int>.json`
    - der neueste Index-Datei (`29.json`) ist im Repo enthalten
- `generate_sound_pack.py`:
    - nimmt alle Dateien im `sounds`-Ordner, konvertiert sie nach Möglichkeit zu `.ogg` und generiert ein Sound-Pack mit der Ordnerstruktur, die Minecraft erwartet
    - die Dateinamen müssen dazu ein bestimmtes Format haben: 
        1. `<eigener_name>__`:
            - dieser Teil ist optional und kann dazu dienen verschidene Sounds auseinander zu halten
            - er wird vom Script ignoriert
        2. `<sound_path>.<extension>`:
            - `<sound_path>` ist hier der Pfad, den der Sound in der Ordnerstruktur haben soll, wobei `/` durch `-` ersetzt wurden
            - alle möglichen Pfade können der `sounds_<int>.json` entnommen werden
            - `<extension>` sollte eine valide Dateiendung einer Audiodatei sein, das Script nutzt diese, um die Datei in eine `.ogg` zu konvertieren
            - andere Dateien, wie `.txt`, sollten deshalb nicht im `sounds`-Ordner liegen
    - das Script überprüft außerdem, ob die Sound-Pfade tatsächlich in Minecraft existieren (indem es sie mit einer `sound_<int>.json` vergleicht)
    - falls mehrere Dateien mit gleichem `sound_path` in `sounds` definiert sind fügt das script diese als verschiede Varianten des selben Sounds ein (fortlaufend nummeriert mit 1, 2, etc.)
    - es übeprüft auch, dass die Anzahl an Varianten nicht die maximale Anzahl übersteigt, die es für diesen Sound gibt
    - ###  Beispiele für valide Dateinamen:
        - `mob-zombie-hurt.mp3`
        - `hello_there__mob-zombie-hurt.mp3`
        - `yaaay__mob-vindication_illager-celebrate.mp3`
        - `yaaay2__mob-vindication_illager-celebrate.ogg`

# Requirements: 
- python
- python packages:
    - pydub
    - os, re und json (sollten per default mit dabei sein)
- entweder avconv oder ffmpeg für die Konvertierung
    - ffmpeg konnte ich relativ einfach von der commmandline installieren mit:
        ```
        pip install ffmpeg-downloader
        ffdl install --add-path
        ```