# Minit Randomizer Setup Guide

## Required Software

- Minit installed
	- tested with [Steam](https://store.steampowered.com/app/609490/Minit/), and Epic games
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a YAML file?

You can customize your options by visiting the [Minit Player Options Page](../player-options)

## Joining a MultiWorld Game

### Launching the Minit Client

Minit Client is avaliable in ArchipelagoLauncher.exe, which will open up a pop-up Client when clicked. The room Url:Port can then be entered into the server box and Connect will connect the client to the room.

### Patching the game

Game patches only need to be done when there is a game update. But to do so you can run /Patch in the Minit Client and choose the data.win file in your Minit install folder. When the process is complete the client will respond with "Patched."

Note: You may want to patch a seperate copy of your Minit installation, if you do you can simply choose the copy's data.win instead.

If the chosen data.win file does not match a known vanilla minit hash the client will respond with "Selected game is not vanilla, please reset the game and repatch". If this happens, reinstalling the game and re-running the /Patch command will be necessary.

### Running the game

With the Minit Client open and connected and the data.win patched, simply running Minit.exe and starting a new game will connect the game to the room. If you already have a save file for this room opening that save file will do the same.
