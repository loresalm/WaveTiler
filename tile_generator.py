from PIL import Image, ImageDraw
import os


def create_blank_tile(size, save_path):
    turquoise = (64, 224, 208)  # RGB for turquoise
    tile = Image.new('RGB', (size, size), turquoise)
    tile.save(save_path)


def create_full_tile(size, save_path):
    black = (0, 0, 0)  # RGB for turquoise
    tile = Image.new('RGB', (size, size), black)
    tile.save(save_path)


def create_striped_tile(size, save_path):
    turquoise = (64, 224, 208)  # RGB for turquoise
    tile = Image.new('RGB', (size, size), turquoise)
    draw = ImageDraw.Draw(tile)
    draw.rectangle([0, 4, 12, 7], fill='black')
    tile.save(save_path)


def create_cross_tile(size, save_path):
    turquoise = (64, 224, 208)  # RGB for turquoise
    tile = Image.new('RGB', (size, size), turquoise)
    draw = ImageDraw.Draw(tile)
    draw.rectangle([4, 0, 7, 12], fill='black')
    draw.rectangle([0, 4, 12, 7], fill='black')
    tile.save(save_path)


def create_oblique_tile(size, save_path):
    tile = Image.new('RGB', (size, size), 'turquoise')
    draw = ImageDraw.Draw(tile)
    draw.rectangle([7, 0, 12, 12], fill='black')
    draw.rectangle([3, 2, 7, 9], fill='black')
    draw.rectangle([0, 4, 12, 7], fill='black')
    tile.save(save_path)


def create_corner_tile(size, save_path):
    tile = Image.new('RGB', (size, size), 'turquoise')
    draw = ImageDraw.Draw(tile)
    draw.rectangle([4, 5, 7, 12], fill='black')
    draw.rectangle([0, 4, 6, 7], fill='black')
    tile.save(save_path)


def create_start_tile(size, save_path):
    tile = Image.new('RGB', (size, size), 'turquoise')
    draw = ImageDraw.Draw(tile)
    draw.rectangle([0, 4, 6, 7], fill='black')
    tile.save(save_path)


def main():
    tile_size = 12
    output_dir = 'data/set3/'
    os.makedirs(output_dir, exist_ok=True)
    
    blank_tile_path = os.path.join(output_dir, 'blank_tile.png')
    full_tile_path = os.path.join(output_dir, 'full_tile.png')
    striped_tile_path = os.path.join(output_dir, 'striped_tile.png')
    cross_tile_path = os.path.join(output_dir, 'cross_tile.png')
    oblique_tile_path = os.path.join(output_dir, 'oblique_tile.png')
    corner_tile_path = os.path.join(output_dir, 'corner_tile.png')
    start_tile_path = os.path.join(output_dir, 'start_tile.png')
    
    create_blank_tile(tile_size, blank_tile_path)
    create_striped_tile(tile_size, striped_tile_path)
    create_cross_tile(tile_size, cross_tile_path)
    create_full_tile(tile_size, full_tile_path)
    create_oblique_tile(tile_size, oblique_tile_path)
    create_corner_tile(tile_size, corner_tile_path)
    create_start_tile(tile_size, start_tile_path)
    
    print(f'Tiles saved in {output_dir}')

if __name__ == "__main__":
    main()
