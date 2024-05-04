Notes from Colin Vo

Hi! At the time of writing this, I am pretty new to NixOS so I'm not entirely
sure if there's a good workaround for what I'm trying to do. 

To start the program, open a terminal and enter the following:

./init.sh

If it doesn't work, you will need to give it execute permissions by doing:

sudo chmod +x init.sh

Then, in the top left corner of the screen, choose Applications and log out and log back in.
Once you are logged back in, enter the following:

nix-shell shell.nix
python drone_monitor.py

From here, the program is good to go. I couldn't get the background image to stay as a background
with OpenCV so my temporary solution is to open the image in the NixOS file viewer and fullscreen it.

Once that is done, you're good to go! (To exit, CTRL+C)


PS: The videos can be easily changed, just need to be renamed to vidx where x is the number of the video.
The videos are stored locally on the PC at RMSC.
