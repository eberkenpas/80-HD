#!/bin/bash

echo "Committing changes..."
git commit -a -m "stray commit"

echo "Pushing to repository..."
git push

echo "Connecting to Raspberry Pi and running main.py..."

echo "Press Ctrl+C to quit and return to host"
ssh pi@192.168.50.74 "cd /home/pi/pyPro/80-HD/Source && git pull && python3 main.py"

echo "Returned to host machine"

