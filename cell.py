from tile import Tile
import random
import os
from PIL import Image
import time


class Cell:
    def __init__(self, position, possible_tiles):
        self.position = position
        self.possible_tiles = set(possible_tiles)
        self.possible_tiles_id = set()
        for t in possible_tiles:
            self.possible_tiles_id.add(t.id)
        self.collapsed_tile = None
        self.neighbors = {"top": None, "bottom": None, "left": None, "right": None}
        self.is_collapsed = False

    def set_neighbor(self, direction, neighbor_cell):
        if direction in self.neighbors:
            self.neighbors[direction] = neighbor_cell

    def update_possible_tiles(self, direction):
        neighbor = self.neighbors.get(direction)
        collapsed_tile = neighbor.collapsed_tile
        opposite = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
        compatible_tiles = collapsed_tile.compatible_tiles[opposite[direction]]
        common_tiles = self.possible_tiles_id.intersection(compatible_tiles)
        if common_tiles:
            new_tiles = set()
            self.possible_tiles_id = common_tiles
            for id in self.possible_tiles_id:
                for t in self.possible_tiles:
                    if t.id == id:
                        new_tiles.add(t)
            self.possible_tiles = new_tiles
            # print(f"tile available for this cell: {self.position}")
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
    def collapse(self):
        print("choice ---> ", list(self.possible_tiles))
        self.possible_tiles = {random.choice(list(self.possible_tiles))}
        self.possible_tiles_id = {list(self.possible_tiles)[0].id}
        self.collapsed_tile = list(self.possible_tiles)[0]
        self.is_collapsed = True

    def entropy(self):
        return len(self.possible_tiles)


def load_tiles(tile_dir):
    tiles = []
    for idx, file in enumerate(os.listdir(tile_dir)):
        i = 0
        off_idx = -1
        if file.endswith((".png", ".jpg", ".jpeg")):
            if file == "off.png":
                off_idx == i
            path = os.path.join(tile_dir, file)
            tile_image = Image.open(path).convert("RGB")
            tiles.append(Tile(tile_image, idx))
            i += 1  
    return tiles, off_idx


def visualize_grid(cells, grid_size, tile_size, tiles, save_path):
    img_size = grid_size * tile_size
    grid_img = Image.new("RGB", (img_size, img_size), (255, 255, 255))
    for row in cells:
        for cell in row:
            if cell.is_collapsed:
                #print(f"{cell.position} --> {cell.entropy()} --> is collapsed")
                tile = list(cell.possible_tiles)[0]
                tile_img = tile.image
                pos_x, pos_y = cell.position[0] * tile_size, cell.position[1] * tile_size
                grid_img.paste(tile_img, (pos_x, pos_y))
            else:
                pass
                #print(f"{cell.position} --> {cell.entropy()}")

    grid_img.save(save_path)


def find_min_entropy(elements):
    print("--> ", elements)
    if len(elements) > 0:
        # Find the minimum entropy value in the list
        min_entropy = min(elements, key=lambda x: x[1])[1]
        # Filter elements that have the minimum entropy
        min_entropy_elements = [element for element in elements if element[1] == min_entropy]
        cell_selected = random.choice(min_entropy_elements)
    else:
        cell_selected = []
    return cell_selected


def main():
    tile_dir = "data/set4/comb/extended"
    output_dir = "data/set4/output"

    # remove all previous outputs 
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        os.remove(file_path)
    while any(os.path.exists(os.path.join(output_dir, f)) for f in os.listdir(output_dir)):
        time.sleep(0.1)

    # load tiles and check compatibility
    tiles, off_idx = load_tiles(tile_dir)
    for t in tiles:
        t.check_tile_compatibility(tiles)

    # pram output
    grid_size = 10
    tile_size = tiles[0].image.size[0]
    max_step = grid_size*grid_size + 1

    # setup cells
    cells = [[Cell((x, y), tiles) for y in range(grid_size)] for x in range(grid_size)]

    # setup neighbors
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
    print("------------")
    print(f"step: {step}")
    visualize_grid(cells, grid_size, tile_size, tiles, f"{output_dir}/step{step}.png")

    # collapsing a cell
    collapse_cell = cells[2][2]

    # loop until the grid is complete
    while True:
        step += 1
        collapse_cell.collapse()

        # check if all cells have been collapsed
        if all(cell.is_collapsed for row in cells for cell in row):
            visualize_grid(cells, grid_size, tile_size, tiles, f"{output_dir}/step{step}.png")
            break

        print("------------")
        print(f"Step {step}:")
        # update the tile in the neighboring cells
        for n in collapse_cell.neighbors:
            if collapse_cell.neighbors[n] is None:
                continue
            else:
                change_dir = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
                collapse_cell.neighbors[n].update_possible_tiles(change_dir[n])

        # select the cell with minimale entropy
        entropy_list = []
        for y, row in enumerate(cells):
            for x, cell in enumerate(row):
                if not cell.is_collapsed:
                    entropy_list.append([cell.position, cell.entropy()])

        coord, _ = find_min_entropy(entropy_list)

        collapse_cell = cells[coord[0]][coord[1]]
        print(f"next to collapse: cell {collapse_cell.position}")
        visualize_grid(cells, grid_size, tile_size, tiles, f"{output_dir}/step{step}.png")

        """
        lowest_entropy_cells = [cell for row in cells for cell in row if not cell.is_collapsed() and cell.entropy() > 0]
        cell_to_collapse = min(lowest_entropy_cells, key=lambda c: c.entropy())
        print(cell_to_collapse.position)
        cell_to_collapse.collapse()
        collapse_list = [cell_to_collapse]
        """
        if all(cell.is_collapsed for row in cells for cell in row):
            break

        if step > max_step:
            print("max step reached")
            break

    print("Grid collapse complete.")

if __name__ == "__main__":
    main()
