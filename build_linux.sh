#!/bin/bash
# Build the Linux version of the application
cd $(dirname "$0")
spotdl_version=$(cat version)
wget https://github.com/spotDL/spotify-downloader/releases/download/v$spotdl_version/spotdl-$spotdl_version-linux
chmod +x spotdl-$spotdl_version-linux
python3 -m pip install pyinstaller
python3 -m PyInstaller --noconfirm --add-data "version:." --onefile --noconsole --icon "src/spotify.ico" --add-data "spotdl-$spotdl_version-linux:." --add-data "src/spotify100.png:."  "main.py" --clean
mv dist/main spotdl
rm -rf build dist main.spec
rm -rf spotdl-$spotdl_version-linux
clear
echo "Linux Build complete!"