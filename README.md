# APMinit
archipelago implementation of a Minit Randomizer

# notes for alpha implementation
i don't have any fanfares for items, picked up or received, but the proxy client will inform you of everything sent and received
the location checks respawn, but getting them again isn't an issue
the game does not automatically sync items, it's currently a manual process (that only works in the initial house) by pressing Q on the keyboard
swords are not handled the best which includes the timer just,, never starting? it might be tied to receiving the cursed sword but i haven't got there yet

# Setup for new Archipelago users

For Installation
Install Archipelago, you will need the generator and likely the server (though the seed can be hosted on Archipelago.gg)
add the minit.apworld file to Archipelago/lib/worlds

For Generation
put a .yaml file (example in Release) into the /Players folder
run ArchipelagoGenerate.exe
it should make a "AP_[numbers].zip" file in /output
that is the file the Server needs, either select it at runtime if hosting locally, or upload to archipelago.gg if hosting on the website

For hosting
run ArchipelagoServer.exe
it will prompt for a seed, choose the previously generated file in /output

For Connecting
run ArchipelagoLauncher.exe
open the "Minit Clint" through the Launcher
use the top bar to enter the host and port of the Archipelago server running already (ex. "localhost:38281" if you are hosting it locally and your port is 38281) 
when prompted for you Slot Name, enter whatever your username in the .yaml file is, if left default it will likely be "Player1"
you now have the proxy client connected to the AP server

For Patching
under Archipelago/Minit (create the folder) put the "data.win" file from your minit install
launch ArchipelagoLauncher.exe, and select "Minit Client"
in the text box of the client that pops up type "/Patch"
take your (now patched) data.win and put it back into your Minit install folder (you can make a copy if you don't want to muck your vanilla game)

# Setup for Archipelago users

.yaml and .apworld are in the Release page and need to be installed appropriatly 
the proxy "Minit Client" can be accessed through ArchipelagoLauncher

you need to patch the game by doing the following:
under Archipelago/Minit (create the folder) put the "data.win" file from your minit install
launch ArchipelagoLauncher.exe, and select "Minit Client"
in the text box of the client that pops up type "/Patch"
take your (now patched) data.win and put it back into your Minit install folder (you can make a copy if you don't want to muck your vanilla game)

