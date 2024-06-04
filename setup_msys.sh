pacman -Suy
pacman -S mingw-w64-ucrt-x86_64-gtk3 mingw-w64-ucrt-x86_64-python3 mingw-w64-ucrt-x86_64-python3-gobject
python3 -m ensurepip
python3 -m pip install -r requirements.txt
