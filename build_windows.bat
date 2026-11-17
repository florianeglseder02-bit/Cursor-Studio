@echo off
cd /d "%~dp0"
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m PyInstaller --noconfirm --clean --windowed --name CursorStudio --add-data "assets;assets" cursor_studio.py
 echo.
echo Fertig! Die Anwendung liegt unter dist\CursorStudio\CursorStudio.exe
echo Du kannst den gesamten Ordner dist\CursorStudio weitergeben.
pause
