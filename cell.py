from tile import Tile
import random
import os
from PIL import Image


class Cell:
    def __init__(self, position, possible_tiles):
        self.position = position
        self.possible_tiles = set(possible_tiles)
        self.possible_tiles_id = set()
        for t in possible_tiles:
            self.possible_tiles_id.add(t.id)
        self.collapsed_tile = None
        self.neighbors = {"top": None, "bottom": None, "left": None, "right": None}

    def set_neighbor(self, direction, neighbor_cell):
        if direction in self.neighbors:
            self.neighbors[direction] = neighbor_cell

    def update_possible_tiles(self, direction):
        neighbor = self.neighbors.get(direction)
        collapsed_tile = neighbor.collapsed_tile
        opposite = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
        compatible_tiles = collapsed_tile.compatible_tiles[direction]
        common_tiles = self.possible_tiles_id.intersection(compatible_tiles)
        if common_tiles:
            new_tiles = set()
            self.possible_tiles_id = common_tiles
            for id in self.possible_tiles_id:
                for t in self.possible_tiles:
                    if t.id == id:
                        new_tiles.add(t)
            self.possible_tiles = new_tiles
            print(f"tile available for this cell: {self.position}")
        else:
            self.possible_tiles_id = set()
            self.possible_tiles = set()
            print(f"no tile available for this cell: {self.position}")

        """
        if neighbor and neighbor.is_collapsed():
            collapsed_tile = list(neighbor.possible_tiles)[0]
            updated_tiles = set(tile for tile in self.possible_tiles if collapsed_tile in tile.compatible_tiles[direction])
            if updated_tiles != self.possible_tiles:
                self.possible_tiles = updated_tiles
                return True
        return False
        """

    def is_collapsed(self):
        return len(self.possible_tiles) == 1

    def collapse(self, chosen_tile=None):
        if chosen_tile and chosen_tile in self.possible_tiles:
            self.possible_tiles = {chosen_tile}
            self.possible_tiles_id = {chosen_tile.id}
        elif not self.is_collapsed():
            self.possible_tiles = {random.choice(list(self.possible_tiles))}
            self.possible_tiles_id = {list(self.possible_tiles)[0].id}
        self.collapsed_tile = list(self.possible_tiles)[0]
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
            print(f"{cell.position} --> {cell.entropy()}")
            if cell.is_collapsed():
                print(f"cell : {cell.position} is collapsed")
                tile = list(cell.possible_tiles)[0]
                tile_img = tile.image
                pos_x, pos_y = cell.position[0] * tile_size, cell.position[1] * tile_size
                grid_img.paste(tile_img, (pos_x, pos_y))
    grid_img.save(save_path)


def main():
    tile_dir = "data/set2/extended"
    output_dir = "data/set2/output"
    tiles = load_tiles(tile_dir)
    for t in tiles:
        t.check_tile_compatibility(tiles)
    grid_size = 3
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

    step = 0
    visualize_grid(cells, grid_size, tile_size, tiles, f"{output_dir}/step{step}.png")
    print(f"Step {step}: Next collapsed cell saved as 'step{step}.png'")

    collapse_cell = cells[0][0]
    collapse_cell.collapse(tiles[0])

    collapse_list = [collapse_cell]

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
        visualize_grid(cells, grid_size, tile_size, tiles, f"{output_dir}/step{step}.png")
        print(f"Step {step}: Next collapsed cell saved as 'step{step}.png'")
        
        lowest_entropy_cells = [cell for row in cells for cell in row if not cell.is_collapsed() and cell.entropy() > 0]
        cell_to_collapse = min(lowest_entropy_cells, key=lambda c: c.entropy())
        print(cell_to_collapse.position)
        cell_to_collapse.collapse()
        collapse_list = [cell_to_collapse]
        if all(cell.is_collapsed() or cell.entropy() == 0 for row in cells for cell in row):
            break

    print("Grid collapse complete.")

if __name__ == "__main__":
    main()
