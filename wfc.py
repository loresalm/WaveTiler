import os
import random
from collections import Counter
from PIL import Image
import numpy as np


class WaveTiler:
    def __init__(self, tile_dir, output_size, pattern_size=2):
        self.tile_dir = tile_dir
        self.output_size = output_size  # (width, height) in tiles
        self.tiles, self.tile_size = self.load_tiles()
        self.pattern_size = self.tile_size[0]
        self.patterns, self.pattern_weights = self.extract_patterns()

    def load_tiles(self):
        tiles = []
        tile_sizes = set()
        for file in os.listdir(self.tile_dir):
            if file.endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(self.tile_dir, file)
                tile = Image.open(path).convert('RGB')
                tile_sizes.add(tile.size)
                tiles.append(tile)

        if len(tile_sizes) != 1:
            raise ValueError("All tiles must have the same size.")

        tile_size = tile_sizes.pop()
        return tiles, tile_size

    def extract_patterns(self):
        patterns = []
        for tile in self.tiles:
            tile_array = np.array(tile)
            for y in range(tile_array.shape[0] - self.pattern_size + 1):
                for x in range(tile_array.shape[1] - self.pattern_size + 1):
                    pattern = tile_array[y:y+self.pattern_size,
                                         x:x+self.pattern_size]
                    patterns.append(pattern.tobytes())
        pattern_counts = Counter(patterns)
        pattern_images = [
            Image.fromarray(
                np.frombuffer(p, dtype=np.uint8).reshape((self.pattern_size, self.pattern_size, 3))) for p in pattern_counts]
        return pattern_images, list(pattern_counts.values())

    def observe(self, wave):
        entropies = [len(states) for states in wave]
        min_entropy = min([e for e in entropies if e > 1], default=None)
        if min_entropy is None:
            return None
        choices = [i for i, e in enumerate(entropies) if e == min_entropy]
        return random.choice(choices)

    def collapse(self, wave, index):
        wave[index] = [random.choices(self.patterns, 
                       weights=self.pattern_weights)[0]]

    def propagate(self, wave):
        # Simplified propagation without constraints for now
        pass

    def generate_image(self):
        wave = [
            [pattern for pattern in self.patterns]
            for _ in range(self.output_size[0] * self.output_size[1])]
        while True:
            index = self.observe(wave)
            if index is None:
                break
            self.collapse(wave, index)
            self.propagate(wave)

        output_width = self.output_size[0] * self.pattern_size
        output_height = self.output_size[1] * self.pattern_size
        output_image = Image.new('RGB', (output_width, output_height))

        for i, state in enumerate(wave):
            x = (i % self.output_size[0]) * self.pattern_size
            y = (i // self.output_size[0]) * self.pattern_size
            output_image.paste(state[0], (x, y))

        return output_image

    def save_image(self, output_path):
        image = self.generate_image()
        image.save(output_path, 'PNG')


if __name__ == "__main__":
    tile_directory = "data/set2/"
    output_file = "data/output/generated_image.png"
    output_grid_size = (10, 10)  # 10x10 tiles

    generator = WaveTiler(tile_directory, output_grid_size)
    generator.save_image(output_file)
    print(f"Generated image saved as {output_file}")
