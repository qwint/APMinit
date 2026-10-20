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
* The Box to the left of the Press Pass room will respawn.
* In Entrance Rando the Temple Coin puzzle will not require the deaths to happen in the temple room.

## Setup for new Archipelago users

### For Installation
* Install Archipelago, you will need the generator and likely the server
  (though the seed can be hosted on Archipelago.gg).
* Add the minit.apworld file to Archipelago/custom_worlds.
* Archipelago Minit Mod and Minit Mod Loader (further details in `For Patching` section)
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
* When prompted for your Slot Name, enter whatever your username in the .yaml file is,
  if left default it will likely be "Player1".
* You now have the proxy client connected to the AP server


### For Patching
* Install the Mod Loader
  * download from https://github.com/qwint/UFO-50-MOD-LOADER/releases
  * unzip the appropriate version to a reasonable location, run `minit Mod Loader` to open the Mod Loader
* Install the Minit Mod into the Mod Loader
  * download `Source code (zip)` from https://github.com/qwint/archipelago_minit_mod/releases
  * Launch the Mod Loader
  * under `Mod Loader` select `Open Mod Loader Folder`
  * Open the `Minit mods` subfolder and place the downloaded zip
* Patch the game
  * Launch the Mod Loader
  * Optional: Under `Settings` you can check `Overwrite Installed Files` to patch the source copy of the game
  * Check the installed Minit mod to include it
  * Press the `Load Mods and Launch Game` button
* Run the game
  * The previous step will automatically launch the game, but to not need to patch every time you can either
    * Use the `Overwrite Installed Files` setting and launch through your previous launcher of choice
    * Run the modded copy directly, it will be in `./workspace/Minit Modded Copy/minit.exe` from the same Mod Loader Folder as before
      * On linux the Mod Loader runs the game through `wine` so it is safe to do so manually as well
    * Open the Mod Loader and press the `Launch Game` button

## Setup for Archipelago users

* minit.apworld is in the Release page and needs to be installed appropriatly.
* tracker.apworld (for Universal Tracker, installed seperately) can add a new tab to the client that functions as
  a simple location tracker.
* The proxy "Minit Client" can be accessed through ArchipelagoLauncher.
* Download the Archipelago Minit Mod and patch through the Mod Loader.
  For more detail see the `For Patching` section above.
