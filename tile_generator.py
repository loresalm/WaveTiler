from PIL import Image, ImageDraw
import os

def create_blank_tile(size, save_path):
    turquoise = (64, 224, 208)  # RGB for turquoise
    tile = Image.new('RGB', (size, size), turquoise) 
    tile.save(save_path)

def create_striped_tile(size, save_path):
    turquoise = (64, 224, 208)  # RGB for turquoise
    tile = Image.new('RGB', (size, size), turquoise)
    draw = ImageDraw.Draw(tile)
    draw.rectangle([0, 4, 11, 7], fill='black')
    tile.save(save_path)

def main():
    tile_size = 12
    output_dir = 'data/set2/'
    os.makedirs(output_dir, exist_ok=True)
    
    blank_tile_path = os.path.join(output_dir, 'blank_tile.png')
    striped_tile_path = os.path.join(output_dir, 'striped_tile.png')
    
    create_blank_tile(tile_size, blank_tile_path)
    create_striped_tile(tile_size, striped_tile_path)
    
    print(f'Tiles saved in {output_dir}')

if __name__ == "__main__":
    main()
