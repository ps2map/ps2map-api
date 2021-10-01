"""Unit tests for map tile extractor tests."""

import unittest

from tools.map_tile_extractor import (  # pylint: disable=import-error
    _map_tile_count as map_tile_count,  # type: ignore
    _map_step_size as map_step_size,  # type: ignore
    _map_grid_limits as map_grid_limits  # type: ignore
)


class TileGridTests(unittest.TestCase):
    """Grid navigation and LOD compensation code."""

    def test_map_tile_count(self) -> None:
        """Test the number of tiles for each LOD."""
        tile_count = map_tile_count
        with self.subTest('Size: 8192'):
            self.assertEqual(tile_count(8192, 0), 1024)
            self.assertEqual(tile_count(8192, 1), 256)
            self.assertEqual(tile_count(8192, 2), 64)
            self.assertEqual(tile_count(8192, 3), 16)
        with self.subTest('Size: 4096'):
            self.assertEqual(tile_count(4096, 0), 256)
            self.assertEqual(tile_count(4096, 1), 64)
            self.assertEqual(tile_count(4096, 2), 16)
            self.assertEqual(tile_count(4096, 3), 4)
        with self.subTest('Size: 2048'):
            self.assertEqual(tile_count(2048, 0), 64)
            self.assertEqual(tile_count(2048, 1), 16)
            self.assertEqual(tile_count(2048, 2), 4)
            self.assertEqual(tile_count(2048, 3), 1)
        with self.subTest('Size: 1024'):
            self.assertEqual(tile_count(1024, 0), 16)
            self.assertEqual(tile_count(1024, 1), 4)
            self.assertEqual(tile_count(1024, 2), 1)
            self.assertEqual(tile_count(1024, 3), 1)

    def test_map_step_size(self) -> None:
        """Test the grid cell width for each LOD."""
        step_size = map_step_size
        with self.subTest('Size: 8192'):
            self.assertEqual(step_size(8192, 0), 4)
            self.assertEqual(step_size(8192, 1), 8)
            self.assertEqual(step_size(8192, 2), 16)
            self.assertEqual(step_size(8192, 3), 32)
        with self.subTest('Size: 4096'):
            self.assertEqual(step_size(4096, 0), 4)
            self.assertEqual(step_size(4096, 1), 8)
            self.assertEqual(step_size(4096, 2), 16)
            self.assertEqual(step_size(4096, 3), 32)
        with self.subTest('Size: 2048'):
            self.assertEqual(step_size(2048, 0), 4)
            self.assertEqual(step_size(2048, 1), 8)
            self.assertEqual(step_size(2048, 2), 16)
            self.assertEqual(step_size(2048, 3), 16)
        with self.subTest('Size: 1024'):
            self.assertEqual(step_size(1024, 0), 4)
            self.assertEqual(step_size(1024, 1), 8)
            self.assertEqual(step_size(1024, 2), 8)
            self.assertEqual(step_size(1024, 3), 8)

    def test_grid_limits(self) -> None:
        """Test the grid limits for each LOD."""
        with self.subTest('Size: 8192'):
            self.assertTupleEqual(map_grid_limits(8192, 0), (-64, 60))
            self.assertTupleEqual(map_grid_limits(8192, 1), (-64, 56))
            self.assertTupleEqual(map_grid_limits(8192, 2), (-64, 48))
            self.assertTupleEqual(map_grid_limits(8192, 3), (-64, 32))
        with self.subTest('Size: 4096'):
            self.assertTupleEqual(map_grid_limits(4096, 0), (-32, 28))
            self.assertTupleEqual(map_grid_limits(4096, 1), (-32, 24))
            self.assertTupleEqual(map_grid_limits(4096, 2), (-32, 16))
            self.assertTupleEqual(map_grid_limits(4096, 3), (-32, 0))
        with self.subTest('Size: 2048'):
            self.assertTupleEqual(map_grid_limits(2048, 0), (-16, 12))
            self.assertTupleEqual(map_grid_limits(2048, 1), (-16, 8))
            self.assertTupleEqual(map_grid_limits(2048, 2), (-16, 0))
            self.assertTupleEqual(map_grid_limits(2048, 3), (-16, -16))
        with self.subTest('Size: 1024'):
            self.assertTupleEqual(map_grid_limits(1024, 0), (-8, 4))
            self.assertTupleEqual(map_grid_limits(1024, 1), (-8, 0))
            self.assertTupleEqual(map_grid_limits(1024, 2), (-8, -8))
            self.assertTupleEqual(map_grid_limits(1024, 3), (-8, -8))
