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

    def update_possible_tiles(self, direction):
        neighbor = self.neighbors.get(direction)
        if neighbor and neighbor.is_collapsed():
            collapsed_tile = list(neighbor.possible_tiles)[0]
            updated_tiles = set(tile for tile in self.possible_tiles if collapsed_tile in tile.compatible_tiles[direction])
            if updated_tiles != self.possible_tiles:
                self.possible_tiles = updated_tiles
                return True
        return False

    def is_collapsed(self):
        return len(self.possible_tiles) == 1

    def collapse(self, chosen_tile=None):
        if chosen_tile and chosen_tile in self.possible_tiles:
            self.possible_tiles = {chosen_tile}
        elif not self.is_collapsed():
            self.possible_tiles = {random.choice(list(self.possible_tiles))}

    def entropy(self):
        return len(self.possible_tiles)

def load_tiles(tile_dir):
    tiles = []
    for idx, file in enumerate(os.listdir(tile_dir)):
        if file.endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(tile_dir, file)
            tile_image = Image.open(path).convert("RGB")
            tiles.append(Tile(tile_image, idx))
    return tiles

def visualize_grid(cells, grid_size, tile_size, tiles, save_path):
    img_size = grid_size * tile_size
    grid_img = Image.new("RGB", (img_size, img_size), (255, 255, 255))
    for row in cells:
        for cell in row:
            if cell.is_collapsed():
                tile = list(cell.possible_tiles)[0]
                tile_img = tile.image
                pos_x, pos_y = cell.position[0] * tile_size, cell.position[1] * tile_size
                grid_img.paste(tile_img, (pos_x, pos_y))
    grid_img.save(save_path)

def main():
    tile_dir = "data/set2/extended"
    tiles = load_tiles(tile_dir)
    grid_size = 2
    tile_size = tiles[0].image.size[0]

    cells = [[Cell((x, y), tiles) for y in range(grid_size)] for x in range(grid_size)]

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

    collapse_cell = cells[1][0]
    collapse_cell.collapse(tiles[0])

    collapse_list = [collapse_cell]

    step = 1
    visualize_grid(cells, grid_size, tile_size, tiles, f"step{step}.png")
    for row in cells:
        for cell in row:
            print(f"{cell.position} --> {cell.entropy()}")

    print("Step 1: Initial collapse saved as 'step1.png'")

    change_dir = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}

    while True:
        step += 1
        print(f"Step {step}:")
        for cell in collapse_list:
            for n in cell.neighbors:
                if cell.neighbors[n] is None:
                    continue
                else:
                    cell.neighbors[n].update_possible_tiles(change_dir[n])
        """
        for row in cells:
            for cell in row:
                print(f"{cell.position} --> {cell.entropy()}")
                for direction in ["top", "bottom", "left", "right"]:
                    cell.update_possible_tiles(direction)
        """

        lowest_entropy_cells = [cell for row in cells for cell in row if not cell.is_collapsed() and cell.entropy() > 0]
        cell_to_collapse = min(lowest_entropy_cells, key=lambda c: c.entropy())
        print(cell_to_collapse.position)
        cell_to_collapse.collapse()
        collapse_list = [cell_to_collapse]
        visualize_grid(cells, grid_size, tile_size, tiles, f"step{step}.png")
        print(f"Step {step}: Next collapsed cell saved as 'step{step}.png'")
        for row in cells:
            for cell in row:
                print(f"{cell.position} --> {cell.entropy()}")

        if all(cell.is_collapsed() or cell.entropy() == 0 for row in cells for cell in row):
            break

    print("Grid collapse complete.")

if __name__ == "__main__":
    main()
