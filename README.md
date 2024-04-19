# APMinit
archipelago implementation of a Minit Randomizer

# What is different from the vanilla game?

* There is an extra location available: you can water the Dolphin NPC south of the Watering Can vanilla location to spawn a heart.
* Regardless of mode both Camera and PressPass will be treated as the same Location, but only PressPass is in the item pool.
* The camera pickup location near your current House is an AP Item that will sync your inventory with the remote server.
* If you have received a remote item from the Archipelago Server, it does not sync automatically into your inventory. You are expected to sync your inventory with the AP Item near the house. Local items will automatically be added to your inventory though.
* An extra keybind has been added (currently only on keyboard Q) to respawn at the Start Location.

# Setup for new Archipelago users

For Installation
Install Archipelago, you will need the generator and likely the server (though the seed can be hosted on Archipelago.gg)
add the minit.apworld file to Archipelago/lib/worlds
the tracker.apworld file can also be installed in the same way, which adds a new tab to the client that functions as a simple location tracker

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
open the "Minit Client" through the Launcher
use the top bar to enter the host and port of the Archipelago server running already (ex. "localhost:38281" if you are hosting it locally and your port is 38281) 
when prompted for you Slot Name, enter whatever your username in the .yaml file is, if left default it will likely be "Player1"
you now have the proxy client connected to the AP server

For Patching
in the text box of the client that pops up type "/Patch", it will prompt you for the data.win file that is in your Minit installation. If the client does not have access to that folder unexpected things may happen, so having a copy of your Minit folder for AP and pointing it there may be safer.
your (now patched) data.win is now ready and installed, only needing to launch the .exe to run the patched game.

# Setup for Archipelago users

.yaml and .apworld are in the Release page and need to be installed appropriatly 
a valid tracker.apworld is also included in the release, which adds a new tab to the client that functions as a simple location tracker
the proxy "Minit Client" can be accessed through ArchipelagoLauncher

you need to patch the game by doing the following:
in the text box of the client that pops up type "/Patch", it will prompt you for the data.win file that is in your Minit installation. If the client does not have access to that folder unexpected things may happen, so having a copy of your Minit folder for AP and pointing it there may be safer.
your (now patched) data.win is now ready and installed, only needing to launch the .exe to run the patched game.

