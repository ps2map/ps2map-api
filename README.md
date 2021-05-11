# APL API Host

Host for the REST and WebSocket API accessed by the front-end.

## Local Dev Version

This version runs locally with no database or other setup needed. Clone this repo and run the following command to host the frontend testing data:

    python -m apl_api

In the local dev version, the API will be hosted at <http://127.0.0.1:5000>.

## Documentation

After launching the API host, a [ReDoc](https://github.com/Redocly/redoc) documentation site will be hosted alongside the API at <http://127.0.0.1:5000/docs>.

## Static File Endpoint

In addition to the REST API, the API server also hosts a number of static assets used to display the game map. These are not covered by the REST API and are instead listed below.

API consumers are also expected to aggressively cache these items due to their large size and frequent access.

### Map Tiles

The map is broken up into tiles of different qualities. This is referred to as the LOD (level-of-detail), with 0 being the highest quality available (8192 px) and higher LOD values halving resolution with each increment; currently the lowest resolution is LOD level 3 (1024 px).

```py
# Number of terrain tiles for a given LOD level:
MAX_LOD = 3
def tiles_by_lod(lod: int) -> int:
    assert 0 <= lod <= MAX_LOD
    return 2 ** (MAX_LOD - lod)

# Size of an individual tile for a given LOD level:
BASE_MAP_SIZE = 8192
def tile_size_by_lod(lod: int) -> int:
    return  BASE_MAP_SIZE / tiles_by_lod(lod)
```

The map tile coordinates originate in the centre and are Cartesian indices with the unit vectors `(1,0)` and `(0,1)` corresponding to east and north respectively.

**Important:** LOD level 3, which only has a single tile, uses the coordinates `(0, 0)`.

The path syntax for accessing tiles is as follows:

    /static/tile/<code>/lod<lod>_<tileX>_<tileY>.jpg

The `<code>` placeholder represents a map-specific asset identifier, generally the lowercase version of the map name. It is recommended to use the `ContinentInfo.code` field from the REST API rather than hard-coding the names if possible.

Tile endpoit example:

    /static/tile/amerish/lod1_2_-2.jpg

### Map Hexes

The map hexes are stored in a single SVG file with all base outlines having their own path. The SVG view box has no offset and a size of 8192 pixels.

Each base outline is stored as a polygon whose `id` matches that of the base it represents.

The path syntax for accessing map hexes is as follows:

    /static/hex/<code>.svg

Example:

    /static/hex/amerish.svg
