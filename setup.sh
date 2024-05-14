
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt update
sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-4.0 python3-pip libcanberra-gtk-module libcanberra-gtk3-module gcc-4.9
sudo apt upgrade libstdc++6
sudo apt dist-upgrade
python3 -m pip install -r requirements.txt
