import os
from PIL import Image
import numpy as np
from tile import Tile


def load_tiles(tile_dir):
    tiles = []
    idx = 0
    for file in os.listdir(tile_dir):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(tile_dir, file)
            tile_image = Image.open(path).convert('RGB')
            tiles.append(Tile(tile_image, idx))
            idx += 1
    return tiles


def check_tile_compatibility(tiles):
    directions = ["top", "bottom", "left", "right"]
    opposite = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
    for tile in tiles:
        for direction in directions:
            tile_edge = tile.get_edge(direction)
            for other_tile in tiles:
                other_edge = other_tile.get_edge(opposite[direction])
                if np.array_equal(tile_edge, other_edge):
                    tile.add_compatible_tile(direction, other_tile.id)


def print_compatibility(tiles):
    for tile in tiles:
        print(f"Tile {tile.id} compatible tiles:")
        for direction, compatible in tile.compatible_tiles.items():
            print(f"  {direction}: {sorted(list(compatible))}")


if __name__ == "__main__":

    tile_set = "set2"
    tile_directory = f"data/{tile_set}/extended"
    tiles = load_tiles(tile_directory)
    check_tile_compatibility(tiles)
    print_compatibility(tiles)

    for tile in tiles:
        save_path = f"data/output/matches/{tile_set}/tile_{tile.id}_compatibility.png"
        tile.visualize_compatibility(tiles, save_path)
        print(f"Compatibility visualization saved as {save_path}")
