#!/bin/bash
# Setup script for Papaya Extra Extensions

echo "Installing Python dependencies for Extensions..."
pip install -r requirements.txt

echo "Checking system dependencies..."
# sys_control might need alsa-utils, usually pre-installed but good to check
if ! command -v amixer &> /dev/null; then
    echo "Warning: 'amixer' not found. Volume control might not work."
    echo "Install alsa-utils (sudo apt install alsa-utils)"
fi

echo "✅ Extensions Setup Complete."
