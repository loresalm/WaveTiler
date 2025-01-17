import os
import random
from collections import Counter
from PIL import Image
import numpy as np


###################
#                 #
#      Tile       #  
#                 #  
###################
class Tile:
    def __init__(self, image, id):
        self.image = image
        self.id = id
        self.compatible_tiles = {"top": set(),
                                 "bottom": set(),
                                 "left": set(),
                                 "right": set()}

    def set_compatibility(self, direction, compatible_tile_ids):
        self.compatible_tiles[direction] = compatible_tile_ids


###################
#                 #
#      Cell       #  
#                 #  
###################
class Cell:
    def __init__(self, possible_tiles):
        self.possible_tiles = set(possible_tiles)
        self.collapsed = False

    def collapse(self):
        if not self.collapsed and self.possible_tiles:
            self.possible_tiles = {random.choice(list(self.possible_tiles))}
            self.collapsed = True

    def reduce_options(self, compatible_tile_ids):
        if not self.collapsed:
            self.possible_tiles &= compatible_tile_ids
            if len(self.possible_tiles) == 1:
                self.collapse()


###################
#                 #
#    WaveTiler    #  
#                 #  
###################
class WaveTiler:
    def __init__(self, tile_dir, output_size, pattern_size=2):
        self.tile_dir = tile_dir
        self.output_size = output_size  # (width, height) in tiles
        self.pattern_size = pattern_size
        self.tiles = self.load_tiles()
        self.grid = self.initialize_grid()

    def load_tiles(self):
        tiles = []
        tile_sizes = set()
        for idx, file in enumerate(os.listdir(self.tile_dir)):
            if file.endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(self.tile_dir, file)
                tile_image = Image.open(path).convert('RGB')
                tile_sizes.add(tile_image.size)
                tiles.append(Tile(tile_image, idx))
        
        if len(tile_sizes) != 1:
            raise ValueError("All tiles must have the same size.")
        return tiles

    def initialize_grid(self):
        possible_tile_ids = set(tile.id for tile in self.tiles)
        return [[Cell(possible_tile_ids) for _ in range(self.output_size[0])] for _ in range(self.output_size[1])]

    def observe(self):
        min_entropy = float('inf')
        target_cell = None
        for row in self.grid:
            for cell in row:
                if not cell.collapsed and 1 < len(cell.possible_tiles) < min_entropy:
                    min_entropy = len(cell.possible_tiles)
                    target_cell = cell
        return target_cell

    def collapse(self, cell):
        cell.collapse()

    def propagate(self):
        # Propagation logic to update neighboring cells
        pass

    def run(self):
        while True:
            cell = self.observe()
            if cell is None:
                break
            self.collapse(cell)
            self.propagate()

    def generate_image(self):
        output_width = self.output_size[0] * self.pattern_size
        output_height = self.output_size[1] * self.pattern_size
        output_image = Image.new('RGB', (output_width, output_height))

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell.collapsed:
                    tile_id = list(cell.possible_tiles)[0]
                    tile_image = self.tiles[tile_id].image
                    output_image.paste(tile_image, (x * self.pattern_size, y * self.pattern_size))
        return output_image

    def save_image(self, output_path):
        image = self.generate_image()
        image.save(output_path, 'PNG')


if __name__ == "__main__":
    tile_directory = "./tiles"
    output_file = "generated_image.png"
    output_grid_size = (10, 10)

    generator = WaveTiler(tile_directory, output_grid_size)
    generator.run()
    generator.save_image(output_file)
    print(f"Generated image saved as {output_file}")
