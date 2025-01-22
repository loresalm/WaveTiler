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

    def check_tile_compatibility(self, tiles):
        directions = ["top", "bottom", "left", "right"]
        opposite = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
        for direction in directions:
            self_edge = self.get_edge(direction)
            for other_tile in tiles:
                other_edge = other_tile.get_edge(opposite[direction])
                if np.array_equal(self_edge, other_edge):
                    self.add_compatible_tile(direction, other_tile.id)

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

        grid_image.save(save_path)
