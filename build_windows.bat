@echo off
@REM Build the windows version of the application
cd "%~dp0"
for /f "delims=" %%a in (version) do set spotdl_version=%%a
set url="https://github.com/spotDL/spotify-downloader/releases/download/v%spotdl_version%/spotdl-%spotdl_version%-win32.exe" 
set file="spotdl-%spotdl_version%-win32.exe"
echo Downloading spotdl bin
powershell -Command "Invoke-WebRequest %url% -OutFile %file%"
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --add-data "version;." --onefile --noconsole --icon "src/spotify.ico" --add-data "spotdl-%spotdl_version%-win32.exe;." --add-data "src/spotify100.png;."  "main.py" --clean
move dist\main.exe spotdl.exe
del /f /q main.spec
rmdir /s /q build
rmdir /s /q dist
del /f /q spotdl-%spotdl_version%-win32.exe
cls
echo Windows Build complete!
