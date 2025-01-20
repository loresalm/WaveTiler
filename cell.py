from tile import Tile
import random
import os
from PIL import Image


class Cell:
    def __init__(self, position, possible_tiles):
        self.position = position
        self.possible_tiles = set(possible_tiles)
        self.neighbors = {"top": None, "bottom": None, "left": None, "right": None}

    def set_neighbor(self, direction, neighbor_cell):
        if direction in self.neighbors:
            self.neighbors[direction] = neighbor_cell

    def update_possible_tiles(self, tile_compatibility):
        updated_tiles = set(self.possible_tiles)
        for direction, neighbor in self.neighbors.items():
            if neighbor is None:
                continue
            compatible_tiles = set()
            for neighbor_tile in neighbor.possible_tiles:
                for tile in self.possible_tiles:
                    if neighbor_tile in tile_compatibility[tile][direction]:
                        compatible_tiles.add(tile)
            updated_tiles &= compatible_tiles
        if updated_tiles != self.possible_tiles:
            self.possible_tiles = updated_tiles
            return True
        return False

    def is_collapsed(self):
        print("len --> ", len(self.possible_tiles))
        return len(self.possible_tiles) == 1

    def collapse(self, chosen_tile=None):
        print("collapsing")
        self.possible_tiles = {random.choice(list(self.possible_tiles))}
        print("tile select: ", self.possible_tiles)
        print("len --> ", len(self.possible_tiles))

    def entropy(self):
        return len(self.possible_tiles)


def load_tiles(tile_dir):
    tiles = []
    for idx, file in enumerate(os.listdir(tile_dir)):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(tile_dir, file)
            tile_image = Image.open(path).convert('RGB')
            tiles.append(Tile(tile_image, idx))
            print(path)
    return tiles


def viz_cell(cell, grid_size, tile_size, save_path, tiles):
    print(cell.possible_tiles)
    img_size = grid_size * tile_size
    grid_img = Image.new('RGB', (img_size, img_size), (255, 255, 255))
    pos_x, pos_y = cell.position[0] * tile_size, cell.position[1] * tile_size
    tile_id = list(cell.possible_tiles)[0]
    tile_img = tiles[tile_id].image
    grid_img.paste(tile_img, (pos_x, pos_y))
    grid_img.save(save_path)


def visualize_grid(cells, grid_size, tile_size, tiles, save_path):
    img_size = grid_size * tile_size
    grid_img = Image.new('RGB', (img_size, img_size), (255, 255, 255))
    for row in cells:
        for cell in row:
            print(f"cell: {cell.position}")
            print(cell.is_collapsed())
            if cell.is_collapsed():
                print("Collappsed")
                tile_id = list(cell.possible_tiles)[0]
                tile_img = tiles[tile_id].image
                pos_x, pos_y = cell.position[0] * tile_size, cell.position[1] * tile_size
                grid_img.paste(tile_img, (pos_x, pos_y))
    grid_img.save(save_path)


def main():
    tile_dir = "data/set1/extended"
    tiles = load_tiles(tile_dir)
    tile_ids = [tile.id for tile in tiles]
    grid_size = 3
    tile_size = tiles[0].image.size[0]

    cells = [[Cell((x, y), tile_ids) for y in range(grid_size)] for x in range(grid_size)]
    for x in range(grid_size):
        for y in range(grid_size):
            print("len --> ", cells[x][y].entropy())

    for x in range(grid_size):
        for y in range(grid_size):
            cell = cells[x][y]
            if y > 0:
                cell.set_neighbor("top", cells[x][y - 1])
            if y < grid_size - 1:
                cell.set_neighbor("bottom", cells[x][y + 1])
            if x > 0:
                cell.set_neighbor("left", cells[x - 1][y])
            if x < grid_size - 1:
                cell.set_neighbor("right", cells[x + 1][y])

    random_cell = cells[random.randint(0, 2)][random.randint(0, 2)]
    random_tile = random.choice(tile_ids)
    print(f"cell selected: {random_cell.position}")
    random_cell.collapse(random_tile)

    """

    for x in range(grid_size):
        for y in range(grid_size):
            cells[x][y].update_possible_tiles({tile.id: tile.compatible_tiles for tile in tiles})

    print("Cell Entropies:")
    for row in cells:
        for cell in row:
            print(f"Cell {cell.position}: Entropy = {cell.entropy()}")
    """
    # visualize_grid(cells, grid_size, tile_size, tiles, "grid_output.png")
    viz_cell(random_cell, grid_size, tile_size, "grid_output.png", tiles)
    print("Grid visualization saved as 'grid_output.png'")


if __name__ == "__main__":
    main()
