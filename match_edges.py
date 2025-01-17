import os
from PIL import Image
import numpy as np


class Tile:
    def __init__(self, image, id):
        self.image = image
        self.id = id
        self.compatible_tiles = {"top": set(), "bottom": set(), "left": set(), "right": set()}

    def get_edge(self, direction):
        array = np.array(self.image)
        if direction == "top":
            return array[0, :, :]
        elif direction == "bottom":
            return array[-1, :, :]
        elif direction == "left":
            return array[:, 0, :]
        elif direction == "right":
            return array[:, -1, :]

    def add_compatible_tile(self, direction, tile_id):
        self.compatible_tiles[direction].add(tile_id)

    def visualize_compatibility(self, tiles, save_path):
        tile_size = self.image.size[0]
        max_matches = max(len(matches) for matches in self.compatible_tiles.values()) or 1
        nb_cells = (max_matches + 2)
        if nb_cells % 2 == 0:
            nb_cells += 1
        grid_size = tile_size * nb_cells
        grid_image = Image.new('RGB', (grid_size, grid_size), (255, 255, 255))
        center_pos = tile_size * (nb_cells // 2)
        grid_image.paste(self.image, (center_pos, center_pos))

        directions = {
            "top": (1, 0),
            "bottom": (1, max_matches),
            "left": (0, 1),
            "right": (max_matches, 1)
        }

        for direction, (x0, y0) in directions.items():
            compatible_ids = self.compatible_tiles[direction]
            for i, comp_id in enumerate(compatible_ids):

                if direction == "top":
                    offset_y = 0
                    offset_x = tile_size * (1 + i)
                    grid_image.paste(tiles[comp_id].image, (offset_x, offset_y))
                elif direction == "bottom":
                    offset_y = tile_size * (nb_cells - 1)
                    offset_x = tile_size * (1 + i)
                    grid_image.paste(tiles[comp_id].image, (offset_x, offset_y))
                elif direction == "left":
                    offset_y = tile_size * (1 + i)
                    offset_x = 0
                    grid_image.paste(tiles[comp_id].image, (offset_x, offset_y))
                elif direction == "right":
                    offset_y = tile_size * (1 + i)
                    offset_x = tile_size * (nb_cells - 1)
                    grid_image.paste(tiles[comp_id].image, (offset_x, offset_y))

                """
                offset_x =  + dx * tile_size
                offset_y =  + dy * tile_size

                if dx == 0:
                    offset_x += (i - len(compatible_ids) // 2) * tile_size
                else:
                    offset_y += (i - len(compatible_ids) // 2) * tile_size
                """
                # grid_image.paste(tiles[comp_id].image, (offset_x, offset_y))

        grid_image.save(save_path)


def load_tiles(tile_dir):
    tiles = []
    for idx, file in enumerate(os.listdir(tile_dir)):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(tile_dir, file)
            tile_image = Image.open(path).convert('RGB')
            tiles.append(Tile(tile_image, idx))
    return tiles


def check_tile_compatibility(tiles):
    directions = ["top", "bottom", "left", "right"]
    opposite = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
    
    for tile in tiles:
        for direction in directions:
            tile_edge = tile.get_edge(direction)
            for other_tile in tiles:
                if tile.id == other_tile.id:
                    continue
                other_edge = other_tile.get_edge(opposite[direction])
                if np.array_equal(tile_edge, other_edge):
                    tile.add_compatible_tile(direction, other_tile.id)


def print_compatibility(tiles):
    for tile in tiles:
        print(f"Tile {tile.id} compatible tiles:")
        for direction, compatible in tile.compatible_tiles.items():
            print(f"  {direction}: {sorted(list(compatible))}")


if __name__ == "__main__":

    tile_set = "set1"
    tile_directory = f"data/{tile_set}"
    tiles = load_tiles(tile_directory)
    check_tile_compatibility(tiles)
    print_compatibility(tiles)

    for tile in tiles:
        save_path = f"data/output/matches/{tile_set}/tile_{tile.id}_compatibility.png"
        tile.visualize_compatibility(tiles, save_path)
        print(f"Compatibility visualization saved as {save_path}")
