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

import os
import pathlib
import re
import sys
import tempfile
from typing import Iterable, List, Optional, Set

from DbgPack import AssetManager
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
    r'D:\Steam\steamapps\common\PlanetSide 2'
]
# Name of the PS2 executable, used to confirm installation folders
PS2_EXCUTABLE_NAME = 'PlanetSide2_x64.exe'


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


def _convert_image(path: pathlib.Path,
                   output_dir: Optional[pathlib.Path] = None,
                   format_: str = 'png') -> None:
    """Convert a DDS texture asset into a new format.

    By default, this convertex the texture to PNG format. You can
    specify alternate formats via the `format` field. This field is
    used as the file extension when writing the image using pillow
    (<https://pillow.readthedocs.io/en/stable/>). You may specify any
    extension supported by pillow.

    If no output directory is specified, the converted images will be
    placed in the same directory as the source files. Input files must
    be in DDS format and are required to use the "dds" extension (case
    insensitive).

    Args:
        path (pathlib.Path): Path to the input image to read
        output_dir (Optional[pathlib.Path]): Directory to write the
            converted images to
        format_ (str): File extension of the image format to convert the
            files to, see the pillow docs for supported extensions

    Raises:
        RuntimeError: Raised if the given input file is not in DDS
            format or if the `format_` given is not supported

    """
    if os.path.splitext(str(path))[1].lower() != '.dds':
        raise RuntimeError(f'Input file is not in DDS format: {path}')
    # If no output directory was provided, use the input file's directory
    if output_dir is None:
        print('output dir is none')
        output_dir = pathlib.Path(os.path.dirname(path))
    if not os.path.isdir(output_dir):
        raise FileNotFoundError(f'Path is not a directory: {output_dir}')
    # Convert the image
    out_path = output_dir / f'{os.path.basename(path)}.{format_}'
    image = Image.open(path)
    try:
        image.save(out_path)
    except ValueError as err:
        raise RuntimeError(f'Unknown file format: {format_}') from err


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


if __name__ == '__main__':
    output_dir = pathlib.Path('./unpack')
    if not output_dir.exists():
        os.makedirs(output_dir)

    format_ = 'png'
    # TODO: Add --dir switch to allow overriding search locations
    custom_dir = ''

    # Locate the PS2 installation and asset folder
    print('\nLocating PlanetSide 2 install directory...')
    if not custom_dir:
        print(' >> No directory specified, searching common install paths')
    else:
        print(f' >> Using provided installation directory at "{custom_dir}"')
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
    namelist = _get_tile_namelist(data_files)
    print(f' >> done\n >> {len(namelist)} matching assets found')
    if not namelist:
        print('Unable to extract files due to empty namelist')
        sys.exit(1)

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
            manager = AssetManager([asset_dir / archive], namelist=namelist)
            _unpack_files(manager, temp_path)

        # Recombine the small assets into larger blocks
        print('\nMerge tile assets\n >> Not yet implemented, skipping...')
        # TODO: Implement re-merging of map tiles

        # Convert DDS textures into a more friendly format
        if format_ is not None:
            print('\nConverting DDS textures...\n'
                  f' >> Using export format "{format_}"\n')
            images = [pathlib.Path(f) for f in os.listdir(temp_path)]
            total = len(images)
            for index, image in enumerate(images):
                print(f' >> Converting asset {index+1} of {total}: '
                      f'{image}')
                _convert_image(temp_path / image, output_dir, format_)
            print('\n >> done\n')
