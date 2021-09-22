# Tools and Scripts

This directory contains utilities and helper scripts used to maintain the API host. They are generally standalone and not tied to the repository unless specified otherwise.

The requirements for each tool are listed in the sections below. Alternatively you can install the requirements for all utilities using the `requirements.txt` file in this directory.

## Map Hex Generator

A Python script for generating SVGs for the PlanetSide 2 continent maps.

This utility uses "base IDs". These generally match the in-game "map region" IDs.

This utility requires [`auraxium`](https://github.com/leonhard-s/auraxium) version 0.2.0b4 or greater.

### Script

The script portion of this utility generates SVG assets for the four main continents (Indar, Hossin, Amerish, and Esamir). The SVG is generated using a view box of `0 0 8192 8192` with all polygon coordinates matching the in-game coordinate system.

This script sends one request per continent and should stay beneath the API rate limit for single runs. A custom service ID can be specified using the `--service-id` command line switch.

### Module

Alternatively, the module can also be imported and targeted from other Python modules. The only two public methods are the two coroutines `get_base_svgs` and `get_base_outlines.

`get_base_svgs` is the endpoint targeted by the script mode and returns a string literal to be written to an SVG file. `get_base_outlines` returns a mapping of base IDs to coordinates making up that hex outline.

For detailed usage instructions for these methods, please refer to the
corresponding docstrings in the source.

## Map Tile Extractor

A Python script for extracting PlanetSide 2 map tile textures.

Note that this utility requires a local installation of PlanetSide 2 to work. By default, it will search the following common directories for PS2 installations:

- C:\Users\Public\Sony Online Entertainment\Installed Games\PlanetSide 2
- C:\Program Files (x86)\Steam\steamapps\common\PlanetSide 2
- C:\Program Files\PlanetSide 2
- D:\Steam\steamapps\common\PlanetSide 2
- D:\PlanetSide 2

If the PS2 install on the target device does not match any of them, you can specify an alternate installation using the `--dir <dir>` switch.

This utility requires [Pillow](https://python-pillow.org/) version 8.3 or greater.

### Formats

This script supports four modes:

- **raw**: Only extract the map tiles, leaving them as 256 px tiles in DDS format.
- **convert**: Extract the map tiles and export them as 256 px tiles in PNG format.
- ~~**repo**: Export the map tiles and save them as 1024 px JPEG images using the repository's naming scheme.~~ This project will move to the in-game coordinate system soon. As a result, this mode is deprecated and will be replaced soon.
- **merge**: Merge the map tiles into a single large PNG image.

For detailed information on the command line switches available, please refer to the script's help (invoked via the `--help` switch).
