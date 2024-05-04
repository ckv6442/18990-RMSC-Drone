#!/bin/sh

# CV

echo "Hello!"
echo "Adding user: rmsc to group: dialout."
echo "rmsc" | sudo -S usermod -a -G dialout rmsc
echo "Done!"
echo "Giving permission to ttyUSB0 device."
echo "rmsc" | sudo -S chmod ugo+w /dev/ttyUSB0
echo "Done!"
# echo "Starting nix shell. Please wait."


# nix-shell shell.nix

# Tried to get this to execute, need to move this somewhere else.
# echo "Executing Python script."
# python drone_monitor.py