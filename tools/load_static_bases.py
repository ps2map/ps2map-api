"""Base info retrieval utility.

This generates the static JSON base data used for dummy API hosting.

Note that outfit resources are not included on the API and can not be
gathered automatically.

"""

import argparse
import asyncio
import json
import os
from typing import Any

import auraxium


async def main(service_id: str, output_dir: str) -> None:
    """Asynchronous component of the script component."""
    zone_ids = [2, 4, 6, 8]
    bases: list[dict[str, Any]] = []
    async with auraxium.Client(service_id=service_id) as client:
        regions_list = await client.find(
            auraxium.ps2.MapRegion, results=10_000,
            zone_id=','.join((str(i) for i in zone_ids)))
    for region in regions_list:
        bases.append({
            'id': int(region.id),
            'continent_id': int(region.zone_id),
            'name': str(region.facility_name),
            'map_pos': (float(region.location_z or 0.0),
                        float(region.location_x or 0.0)),
            'type_id': int(region.facility_type_id or 0),
            'type_name': str(region.facility_type or 'No Man\'s Land'),
            'resource_amount': 0,
            'resource_id': None,
            'resource_name': None
        })
    bases_sorted = sorted(bases, key=lambda x: x['id'])
    with open(os.path.join(output_dir, 'static_bases.json'),
              'w', encoding='utf-8') as outfile:
        json.dump(bases_sorted, outfile, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--service-id', '-s', default='s:example',
        help='The service ID to use for requests. For once-off script runs, '
        'using the default service ID should not exceed the rate limit')
    parser.add_argument(
        '--output-dir', '-o', default='.',
        help='Output directory to save the exported SVGs to.')
    kwargs = vars(parser.parse_args())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(**kwargs))
