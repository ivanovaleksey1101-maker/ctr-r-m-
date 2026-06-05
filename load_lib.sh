#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -e

detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
    else
        echo "It was not possible to outpace your distro!"
        exit 1
    fi
}

install_ubuntu() {
    echo "Updating packages..."
    sudo apt update
    
    echo "Installing packages for your distro..."
    sudo apt install -y python3 python3-pip python3-venv vlc
    python3 -m venv venv
    source venv/bin/activate
    pip install pygame python-vlc
    
    echo "Complete! To launch game: python3 main.py"
}

install_arch() {
    echo "Installing packages for your distro..."
    sudo pacman -S python python-pip python-virtualenv vlc
    python -m venv venv
    source venv/bin/activate
    pip install pygame python-vlc
    
    echo "Complete! To launch game: python main.py"
}

main() {
    detect_distro
    case $DISTRO in
        ubuntu|debian|linuxmint|pop|elementary|zorin)
            install_ubuntu
            ;;
        arch|manjaro|endeavouros|garuda)
            install_arch
            ;;
    esac
}

main
