# APMinit
archipelago implementation of a Minit Randomizer

## What is different from the vanilla game?

* There is an extra location available: you can water the Dolphin NPC south of the Watering Can vanilla location
  to spawn a heart.
* Regardless of mode both Camera and PressPass will be treated as the same Location,
  but only PressPass is in the item pool.
* If you have received a remote item from the Archipelago Server, it does not sync automatically into your inventory.
  Local items will automatically be added to your inventory but anything recieved off-world will only sync
  after any respawn.
* An extra keybind has been added (currently only on keyboard Q) to respawn at the Start Location.

## Setup for new Archipelago users

### For Installation
* Install Archipelago, you will need the generator and likely the server
  (though the seed can be hosted on Archipelago.gg).
* Add the minit.apworld file to Archipelago/custom_worlds.
* (Optionally) the tracker.apworld file for Universal Tracker can also be installed in the same way,
  which adds a new tab to the client that functions as a simple location tracker

### For Generation
* Put a .yaml file into the /Players folder
    * To locally generate a template you can use `Generate Template Options` from the Archipelago Launcher
    * Alternatively Stripes has offered to host a copy of the Archipelago Webhost that includes Minit
      which can be found at https://ap.stripesoo7.org/games/Minit/player-options
* Run `Generate` from the Archipelago Launcher (or ArchipelagoGenerate.exe directly).
    * On a successul generation it will make a "AP_[numbers].zip" file in /output folder of your AP install

### For Hosting
Use one of the following hosting options
* Run `Host` from the Archipelago Launcher (or ArchipelagoServer.exe directly).
    * It will prompt for a seed, choose the previously generated file in /output
* Go to https://archipelago.gg/uploads and upload the previously generated file in /output


### For Connecting
* Run ArchipelagoLauncher.exe
* Open the "Minit Client" through the Launcher
* Use the top bar to enter the host and port of the Archipelago server running already
  (ex. "localhost:38281" if you are hosting it locally and your port is 38281).
* When prompted for you Slot Name, enter whatever your username in the .yaml file is,
  if left default it will likely be "Player1".
* You now have the proxy client connected to the AP server

### For Patching
In the client there is a `/Patch` command you can use which will automatically create a patched data file
if needed and launch the game when the patching is complete.

The entire process should be automated but in case you need the information for debugging or alternate setups:
* The location of your install will be saved in the `host.yaml` configuration file in your Archipelago Install
* The patched data file will be saved in your minit install folder as `ap_v1.0_data.win`. If you need to manually
  launch then the launch args `-game ap_v1.0_data.win` will work both in a terminal and in steam launch args
  (swap the `v1.0` version for whatever patch version it is).
* If the client does not have access to that folder unexpected things may happen, so having a copy of your Minit folder
  for AP and pointing it there may be safer.

## Setup for Archipelago users

* minit.apworld is in the Release page and needs to be installed appropriatly.
* tracker.apworld (for Universal Tracker, installed seperately) can add a new tab to the client that functions as
  a simple location tracker.
* The proxy "Minit Client" can be accessed through ArchipelagoLauncher.
* The `/Patch` command in the Minit Client will auto patch and launch the patched game.
  For more detail see the `For Patching` section above.
