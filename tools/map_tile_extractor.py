"""Map tile extraction utility.

This script allows exporting the map tile textures from the game files.
This process consists of the following steps:

1. Scraping the game files for any assets whose naming scheme follows
   the pattern used for map tiles. This pattern is configurable via the
   RegEx constant below.
2. Extracting any files identified from the corresponding game archive
   files.
3. (Optional) Merging the individual map tiles into larger tiles more
   suitable to your application.
4. (Optional) Converting the tiles from DDS format to more accessible
   formats like PNG or JPEG.

Important:

Extracting assets from the PlanetSide 2 game files is not covered by
the EULA of PlanetSide 2 or the DayBreak Games API. DBG has generally
displayed goodwill regarding the extraction of assets for creative and
community-focussed purposes, but usage of this utility is still at your
own risk.

"""

# NOTE: The first step in this utility is heavily inspired by
# @RhettVX's "fl_name_scrape" utility in his Forgelight Toolbox:
# <https://github.com/RhettVX/forgelight-toolbox>

import argparse
import dataclasses
import math
import os
import pathlib
import re
import sys
import tempfile
from typing import Dict, Iterable, List, Optional, Set

from DbgPack import AssetManager  # type: ignore
from PIL import Image

# Regular expression used to select the files to scrape for map tiles
FILE_SCRAPE_REGEX = r'(data_x64_\d+.pack2)'
# Regular expression used to identify map tile assets
TILE_ASSET_REGEX = r'(\w+_Tile(_[\d-]\d\d){2}_LOD\d\.((dds)|(DDS)))'

# Files matching these prefixes will not be considered when unpacking
# map assets.
FILE_UNPACK_BLACKLIST = ('assets', 'audio', 'data', 'locale', 'ui')

# Common install directories for PS2 installations
PS2_INSTALL_DIRECTORIES = [
    r'C:\Users\Public\Sony Online Entertainment\Installed Games\PlanetSide 2',
    r'C:\Program Files (x86)\Steam\steamapps\common\PlanetSide 2',
    r'C:\Program Files\PlanetSide 2',
    r'D:\Steam\steamapps\common\PlanetSide 2',
    r'D:\PlanetSide 2'
]
# Name of the PS2 executable, used to confirm installation folders
PS2_EXCUTABLE_NAME = 'PlanetSide2_x64.exe'

# Base size of in-game map tiles
PS2_TILE_SIZE = 256
APL_TILE_SIZE = 1024

# Type aliases
_LodTileMap = Dict[int, List['_MapTile']]


@dataclasses.dataclass()
class _MapTile:
    """Helper object containing map tile data."""

    # pylint: disable=invalid-name

    u: int
    v: int
    lod: int
    path: pathlib.Path


@dataclasses.dataclass()
class _TileMinMax:
    """Helper object storing min/max tile coordinates."""

    min_u: int
    max_U: int
    min_v: int
    max_V: int


def _bytesToString(bytes_: bytes) -> str:
    """Convert a UTF-8 encoded bytes object into a native string.

    Args:
        bytes: UTF-8 encoded bytes object

    Returns:
        string (str): String to convert

    """
    return bytes_.decode('utf-8')


def _strToBytes(string: str) -> bytes:
    """Convert a native string to a UTF-8 encoded bytes object.

    Args:
        string (str): String to convert

    Returns:
        bytes: UTF-8 encoded bytes object

    """
    return bytes(string, 'utf-8')


def _find_game_folder(dir_: Optional[str] = None) -> pathlib.Path:
    """Locate the PlanetSide 2 installation directory.

    This checks a number of common installation directories for the
    PlanetSide 2 executable. Alternatively, the `directory` parameter
    can be used to use that location instead.

    Args:
        dir_ (Optional[str]): Alternate installation directory to use

    Returns:
        A pathlib.Path object pointing at the game's install directory

    Raises:
        FileNotFoundError: Raised if the the PlanetSide 2 installation
            could not be found

    """
    def dir_is_valid(dir_: pathlib.Path) -> bool:
        return os.path.isfile(dir_ / PS2_EXCUTABLE_NAME)
    # Use provided install location if available
    if dir_ is not None:
        dir_path = pathlib.Path(dir_)
        if dir_is_valid(dir_path):
            return dir_path
        raise FileNotFoundError(
            'Unable to find PlanetSide 2 installation at user-provided '
            f'location: {dir_path}')
    # Auto detect location if no directory was specified
    for search_dir in PS2_INSTALL_DIRECTORIES:
        dir_path = pathlib.Path(search_dir)
        if dir_is_valid(dir_path):
            return dir_path
    raise FileNotFoundError(
        'PlanetSide 2 installation not found. Make sure you have the game '
        'installed or use the --dir switch to specify the install directory '
        'containing the "PlanetSide2_x64.exe" executable')


def _get_tile_namelist(paths: Iterable[pathlib.Path]) -> List[str]:
    """Generate a list of tile-like filenames from the given paths.

    These are filenames whose naming pattern matches that of map tile
    assets.

    Args:
        paths (List[pathlib.Path]): List of files to scrape

    Return:
        List[str]: A list of filenames matching the map tile format

    """
    tile_asset_pattern = re.compile(_strToBytes(TILE_ASSET_REGEX))
    namelist: Set[str] = set()
    # Process asset definitions
    manager = AssetManager(list(paths))
    for asset in manager:
        asset_data: bytes = asset.get_data(raw=False)  # type: ignore
        # Filter for file names looking like map tiles
        matches = tile_asset_pattern.findall(asset_data)
        for match in matches:
            filename = match[0]
            namelist.add(_bytesToString(filename))
    return sorted(namelist)


def _unpack_files(manager: AssetManager, output_dir: pathlib.Path) -> None:
    """Unpack select assets from a *.pack2 archive.

    The files to export are selected via the namelist passed to the
    asset manager. Any files not listed in the namelist are ignored and
    will not be exported.

    Args:
        manager (DbgPack.AssetManager): DbgPack asset manager used to
            navigate the archive
        output_dir (pathlib.Path): Output directory to write the
            extracted files to

    """
    for asset in manager.assets.values():
        if not asset.name:
            continue
        # Extract asset to output directory
        asset_data: bytes = asset.get_data(raw=False)  # type: ignore
        (output_dir / asset.name).write_bytes(asset_data)


def _validate_map_tiles(tile_map: _LodTileMap) -> bool:
    """Validate a collection of map tiles.

    This tool ensures the tiles span a valid, square grid without any
    holes.

    Args:
        tile_map (Dict[int, List[_MapTile]]): A collection of map tiles
            to validate

    Returns:
        bool: true if the tiles make up a valid map grid, otherwise
            false

    """
    # Find extreme coordinate values for each map LOD
    extremes: Dict[int, _TileMinMax] = {}
    for lod, tile_list in tile_map.items():
        for tile in tile_list:
            # If the current LOD is not yet stored in the dict, create a dict
            # of initial values
            if not lod in extremes:
                extremes[lod] = _TileMinMax(tile.u, tile.u, tile.v, tile.v)
                continue
            lod_extremes = extremes[lod]
            # Update extreme values
            if tile.u < lod_extremes.min_u:
                lod_extremes.min_u = tile.u
            elif tile.u > lod_extremes.max_U:
                lod_extremes.max_U = tile.u
            if tile.v < lod_extremes.min_v:
                lod_extremes.min_v = tile.v
            elif tile.v > lod_extremes.max_V:
                lod_extremes.max_V = tile.v

    # Validate that each LOD makes up a valid grid
    for lod, lod_extremes in extremes.items():
        # Calculate the step size used in-between tile coordinates
        lod_step_size = 2 ** (lod+2)
        # Ensure the grid is square
        if (lod_extremes.min_u != lod_extremes.min_v
                or lod_extremes.max_U != lod_extremes.max_V):
            return False
        # Create a grid of all tile coordinates to test
        grid: Dict[int, Dict[int, bool]] = {}
        min_, max_ = lod_extremes.min_u, lod_extremes.max_U
        for u in range(min_, max_ + 1, lod_step_size):
            grid[u] = {}
            for v in range(min_, max_ + 1, lod_step_size):
                grid[u][v] = False
        # Update the grid with all coordinates from the map tiles
        for tile in (t for t in tile_map[lod] if t.lod == lod):
            grid[tile.u][tile.v] = True
        # Check the test grid and ensure every position was hit
        for u in range(min_, max_ + 1, lod_step_size):
            for v in range(min_, max_ + 1, lod_step_size):
                if not grid[u][v]:
                    return False
    return True


def _group_tiles(temp_path: pathlib.Path) -> Dict[str, _LodTileMap]:
    """Group map tile assets by map name.

    Args:
        temp_path (pathlib.Path): Directory containing the map tiles

    Returns:
        Dict[str, Dict[int, List[_MapTile]]]: A mapping of nested
            dictionaries. The outer dict key represents the name of the
            map, the inner dictionary groups the map's tiles by LOD
            level.

    """
    map_tiles: Dict[str, Dict[int, List[_MapTile]]] = {}
    for filename in os.listdir(temp_path):
        # Extract tile properties from the asset's filename
        name, _, coord_u, coord_v, lod_str = filename.split('.')[0].split('_')
        lod = int(lod_str[-1])
        tile = _MapTile(int(coord_u), int(coord_v), lod, temp_path / filename)
        # Get the dictionary containing the map tiles
        try:
            lod_tiles = map_tiles[name]
        except KeyError:
            lod_tiles = {}
            map_tiles[name] = lod_tiles
        # Add the tile to the list of tiles for this LOD level
        try:
            lod_tiles[lod].append(tile)
        except KeyError:
            lod_tiles[lod] = [tile]
    return map_tiles


def _merge_tiles(temp_path: pathlib.Path) -> Dict[str, Dict[int, Image.Image]]:
    """Merge all tiles.

    Args:
        temp_path (pathlib.Path): Directory containing the map tiles

    Returns:
        Dict[str, Dict[int, Image.Image]]: A mapping of nested
            dictionaries. The outer dict key represents the name of the
            map, the inner dictionary groups the map's tiles by LOD
            level.
    """
    print(' >> Grouping map tiles...')
    grouped: Dict[str, _LodTileMap] = _group_tiles(temp_path)
    # Generate merged tiles
    output: Dict[str, Dict[int, Image.Image]] = {}
    for name, lod_tiles in grouped.items():
        print(f' >> Merging map tiles for "{name}"...')
        output[name] = {}
        _validate_map_tiles(lod_tiles)
        for lod, tiles in lod_tiles.items():
            merged_size = int(math.sqrt(len(tiles))) * PS2_TILE_SIZE
            img = Image.new('RGB', (merged_size, merged_size))
            for tile in tiles:
                tile_img = Image.open(tile.path)
                tile_u = int((64 + tile.u) / (2 ** (lod+2))) * PS2_TILE_SIZE
                tile_v = int((64 + tile.v) / (2 ** (lod+2))) * PS2_TILE_SIZE
                img.paste(tile_img, (tile_u, tile_v))
            output[name][lod] = img.transpose(Image.FLIP_TOP_BOTTOM)
    return output


def _process_raw(temp_path: pathlib.Path, out_path: pathlib.Path) -> None:
    """Script handler for "raw" format."""
    for filename in os.listdir(temp_path):
        os.rename(temp_path / filename, out_path / filename)


def _process_convert(temp_path: pathlib.Path, out_path: pathlib.Path) -> None:
    """Script handler for "convert" format."""
    files = os.listdir(temp_path)
    total = len(files)
    for index, filename in enumerate(files):
        print(f' >> Converting file {index+1} of {total}')
        outname = filename.rsplit('.', maxsplit=1)[0] + '.png'
        img = Image.open(temp_path / filename)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img.save(out_path / outname)


def _process_apl(temp_path: pathlib.Path, out_path: pathlib.Path) -> None:
    """Script handler for "apl" format."""
    images_merged = _merge_tiles(temp_path)
    for name, lod_images in images_merged.items():
        for lod, image in lod_images.items():
            assert image.height == image.width
            # Calculate the number of slices
            for start_x in range(0, image.height, APL_TILE_SIZE):
                end_x = start_x + APL_TILE_SIZE
                tile_x = start_x / APL_TILE_SIZE - 4
                if start_x >= image.height / 2:
                    tile_x += 1
                for start_y in range(0, image.height, APL_TILE_SIZE):
                    end_y = start_y + APL_TILE_SIZE
                    tile_y = start_y / APL_TILE_SIZE - 4
                    if start_x >= image.height / 2:
                        tile_y += 1
                    img_apl = image.crop((start_x, start_y, end_x, end_y))
                    outname = f'{name}_lod{lod}_{tile_x}_{tile_y}.jpg'
                    print(f' >> Creating tile {outname}')
                    img_apl.save(out_path / outname, quality=95, sampling=0)


def _process_merge(temp_path: pathlib.Path, out_path: pathlib.Path) -> None:
    """Script handler for "merge" format."""
    img_merged: Dict[str, Dict[int, Image.Image]] = _merge_tiles(temp_path)
    for name, map_tiles in img_merged.items():
        for lod, image in map_tiles.items():
            filename = f'{name}_LOD{lod}.png'
            image.save(out_path / filename)


def main(format: str, dir: Optional[str], output: str, namelist: bool) -> None:
    """Main script for tile extraction."""
    # Create the output directory if it does not exist yet
    out_path = pathlib.Path(output)
    if not out_path.exists():
        os.makedirs(out_path)

    # Locate the PS2 installation and asset folder
    print('\nLocating PlanetSide 2 install directory...')
    if dir is None:
        print(' >> No directory specified, searching common install paths')
    else:
        print(f' >> Using provided installation directory at "{dir}"')
    ps2_dir = _find_game_folder()
    print(' >> PlanetSide 2 executable found')
    asset_dir = ps2_dir / 'Resources' / 'Assets'
    print(f' >> Using game assets at "{asset_dir}"')

    # Scrape any *.pack2 data archives for matching assets
    print('\nGenerating namelist...')
    file_regex_pattern = re.compile(FILE_SCRAPE_REGEX)
    data_files = [asset_dir / f for f in os.listdir(asset_dir)
                  if file_regex_pattern.fullmatch(f)]
    print(f' >> Scraping {len(data_files)} archive/s for matching names...')
    names = _get_tile_namelist(data_files)
    print(f' >> done\n >> {len(names)} matching assets found')
    if not names:
        print('Unable to extract files due to empty namelist')
        sys.exit(1)
    if namelist:
        with open(out_path / 'namelist.txt', 'w') as namelist_file:
            namelist_file.writelines((f'{s}\n' for s in names))

    # Unpack all assets in a temporary directory
    print('\nExtracting assets...')
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = pathlib.Path(temp_dir)
        archives = [pathlib.Path(f) for f in os.listdir(asset_dir)
                    if f.endswith('.pack2')
                    and not f.startswith(FILE_UNPACK_BLACKLIST)]
        total = len(archives)
        ignored = [f'{f}*' for f in FILE_UNPACK_BLACKLIST]
        print(f' >> Ignored archives matching: {", ".join(ignored)}\n'
              f' >> Selected {total} archives\n')
        for index, archive in enumerate(archives):
            print(f' >> Extracting archive {index+1} of {total}: {archive}')
            manager = AssetManager([asset_dir / archive], namelist=names)
            _unpack_files(manager, temp_path)

        print(f'\n >> Processing files using format "{format}"...')

        # Recombine the small assets into larger blocks
        if format == 'raw':
            _process_raw(temp_path, out_path)
        elif format == 'convert':
            _process_convert(temp_path, out_path)
        elif format == 'apl':
            _process_apl(temp_path, out_path)
        elif format == 'merge':
            _process_merge(temp_path, out_path)
        else:
            raise RuntimeError(f'Unhandled format: {format}')

        print('\ndone\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'format', default='convert', nargs='?',
        choices=['raw', 'convert', 'apl', 'merge'],
        help='The export format to use. raw: export files in 256 px DDS. '
        'convert: flip files and export them as 256 px PNGs. apl: '
        'export files in 1024 px JPEG. merge: merge all tiles into a '
        'single large PNG image.')
    parser.add_argument(
        '--dir', '-d', nargs=1, default=None, type=str,
        help='The directory containing the PlanetSide 2 executable.')
    parser.add_argument(
        '--output', '-o', nargs=1, default='./map_assets', type=str,
        help='Output directory to save the exported files to.')
    parser.add_argument(
        '--namelist', '-n', action='store_true',
        help='If set, the full namelist will be exported.')
    kwargs = vars(parser.parse_args())

    main(**kwargs)
