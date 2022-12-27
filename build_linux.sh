#!/bin/bash
# Build the Linux version of the application
cd $(dirname "$0")
curl https://github.com/spotDL/spotify-downloader/releases/download/v4.0.6/spotdl-4.0.6-linux -o spotdl-4.0.6-linux
chmod +x spotdl-4.0.6-linux
python3 -m pip install pyinstaller
python3 -m PyInstaller --noconfirm --onefile --console --icon "spotify.ico" --add-data "spotdl-4.0.6-linux:." --add-data "spotify100.png:."  "main.py" --clean
mv dist/main spotdl
rm -rf build dist main.spec
rm -rf spotdl-4.0.6-linux
clear
echo "Linux Build complete!"