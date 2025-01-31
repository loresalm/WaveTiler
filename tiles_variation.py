import os
import shutil
from PIL import Image, ImageChops
import time
import json
import numpy as np

def is_image_equal(img1, img2):
    """Check if two images are identical."""
    diff = ImageChops.difference(img1, img2)
    return diff.getbbox() is None

def highlight_differences(img1, img2):
    """Highlight differences between two images with red pixels."""
    diff = ImageChops.difference(img1, img2)

    # Convert the difference image to an 'L' mode grayscale for use as a mask
    diff_mask = diff.convert('L')

    # Create a red highlight image of the same size
    red_highlight = Image.new("RGB", img1.size, (255, 0, 0))

    # Use the mask to blend the red highlight onto the original image
    combined = Image.composite(red_highlight, img1, diff_mask)
    
    return combined


def create_extended_folder_and_copy_tiles(folder_path):
    """Create the 'extended' folder and copy original tiles to it."""
    extended_folder = os.path.join(folder_path, "extended")
    
    os.makedirs(extended_folder, exist_ok=True)


    # Remove all previous outputs
    for filename in os.listdir(extended_folder):
        file_path = os.path.join(extended_folder, filename)
        os.remove(file_path)
    
    while any(os.path.exists(os.path.join(extended_folder, f)) for f in os.listdir(extended_folder)):
        time.sleep(0.1)

    """
    # Copy all images to the 'extended' folder
    for file in os.listdir(folder_path):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            src = os.path.join(folder_path, file)
            dst = os.path.join(extended_folder, file)
            shutil.copy2(src, dst)
    """

    return extended_folder


def visualize_tile_differences(tile1_path, tile2_path, output_path):
    """
    Visualizes two tiles side by side, highlighting the differing pixels in red.
    Args:
        tile1_path (str): Path to the first tile image.
        tile2_path (str): Path to the second tile image.
        output_path (str): Path to save the output visualization.
    """
    # Open both tile images
    img1 = Image.open(tile1_path).convert('RGB')
    img2 = Image.open(tile2_path).convert('RGB')
    equals = is_image_equal(img1, img2)
    print("--> ", equals)

    # Ensure both images are of the same size
    if img1.size != img2.size:
        raise ValueError("The two tiles must have the same dimensions for comparison.")

    # Compute pixel-wise difference
    diff = ImageChops.difference(img1, img2)
    diff_mask = diff.convert('L')  # Convert to grayscale to use as a mask

    # Create a red overlay where differences are detected
    red_highlight = Image.new("RGB", img1.size, (255, 0, 0))
    highlighted_diff = Image.composite(red_highlight, img1, diff_mask)

    # Combine images side by side
    combined_width = img1.width * 2
    combined_image = Image.new('RGB', (combined_width, img1.height))
    combined_image.paste(img1, (0, 0))
    combined_image.paste(highlighted_diff, (img1.width, 0))

    # Save the result
    combined_image.save(output_path)
    print(f"Difference visualization saved to {output_path}")


def rotate_tile_properties(properties):
    """Rotate the properties of a tile 90 degrees clockwise."""
    return {
            "top": properties["right"],  # Right → Top
            "right": properties["bottom"][::-1],  # Bottom (reversed) → Right
            "bottom": properties["left"],  # Left → Bottom
            "left": properties["top"][::-1],  # Top (reversed) → Left
        }
    """
    return {
        "top": properties["left"],
        "right": properties["top"],
        "bottom": properties["right"],
        "left": properties["bottom"]
    }
    """


def flip_tile_properties(properties, mode):
    """Flip the properties of a tile horizontally or vertically."""
    if mode == "horizontal":
        return {
            "top": properties["top"][::-1],  # Reverse Top
            "right": properties["left"],  # Left → Right
            "bottom": properties["bottom"][::-1],  # Reverse Bottom
            "left": properties["right"],  # Right → Left
        }
        """
        return {
            "top": properties["top"],
            "right": properties["left"],
            "bottom": properties["bottom"],
            "left": properties["right"]
        }
        """
    elif mode == "vertical":
        return {
            "top": properties["bottom"],  # Bottom → Top
            "right": properties["right"][::-1],  # Reverse Right
            "bottom": properties["top"],  # Top → Bottom
            "left": properties["left"][::-1],  # Reverse Left
        }
        """
        return {
            "top": properties["bottom"],
            "right": properties["right"],
            "bottom": properties["top"],
            "left": properties["left"]
        }
        """
    else:
        raise ValueError("Invalid flip mode. Use 'horizontal' or 'vertical'.")


def generate_unique_variations(folder_path, json_path):
    """Generate rotated and mirrored variations of images and save only unique ones."""
    extended_folder = create_extended_folder_and_copy_tiles(folder_path)

    # Load the existing JSON file
    with open(json_path, 'r') as f:
        tile_data = json.load(f)

    variations = []
    for file in os.listdir(folder_path):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            print(file)
            image_path = os.path.join(folder_path, file)
            original = Image.open(image_path)
            tile_name = os.path.splitext(file)[0]

            # Find the corresponding tile properties in the JSON
            tile_properties = None
            for tile in tile_data["tiles"]:
                if tile["tile"] == tile_name:
                    tile_properties = tile
                    break

            if not tile_properties:
                print(f"Warning: No properties found for tile {tile_name}. Skipping.")
                continue

            # Add the original tile and its properties
            variations.append((original, tile_properties, tile_name))

            # Generate rotated versions (90°, 180°, 270°)
            rotated = original
            rotated_properties = tile_properties.copy()
            for _ in range(3):
                rotated = rotated.rotate(90, expand=True)
                rotated_properties = rotate_tile_properties(rotated_properties)
                variations.append((rotated.copy(), rotated_properties.copy(), tile_name))

            # Generate mirrored versions
            flipped_horizontal = original.transpose(Image.FLIP_LEFT_RIGHT)
            flipped_horizontal_properties = flip_tile_properties(tile_properties, "horizontal")
            variations.append((flipped_horizontal, flipped_horizontal_properties, tile_name))

            flipped_vertical = original.transpose(Image.FLIP_TOP_BOTTOM)
            flipped_vertical_properties = flip_tile_properties(tile_properties, "vertical")
            variations.append((flipped_vertical, flipped_vertical_properties, tile_name))

    uniques = []
    unique_properties = []
    for img, properties, tile_name in variations:
        print(tile_name)
        is_unique = True
        print(uniques)
        for unique_img, _, _ in uniques:
            print(img.size, unique_img.size)
            unique_img_ = np.array(unique_img)
            img_ = np.array(img)
            # Check if the arrays are identical
            if np.array_equal(img_, unique_img_):
            #if is_image_equal(img, unique_img):
                print("---> not unique")
                is_unique = False
                break
        if is_unique:
            uniques.append((img, properties, tile_name))
            unique_properties.append(properties)

    # Create a new JSON file for unique variations
    new_json_data = {"tiles": []}

    # Add unique variations to the new JSON file
    count = 1
    for img, properties, tile_name in uniques:
        print(tile_name)
        # Skip the original tiles (only include variations)
        if properties == tile_data["tiles"][0]:  # Check if it's the original tile
            continue

        new_filename = f"{tile_name}_var{count}.png"
        img.save(os.path.join(extended_folder, new_filename))
        print(f"Saved unique variation as {new_filename}")

        # Add the new variation to the new JSON file
        new_tile_entry = {
            "tile": f"{tile_name}_var{count}",
            "top": properties["top"],
            "bottom": properties["bottom"],
            "left": properties["left"],
            "right": properties["right"]
        }
        new_json_data["tiles"].append(new_tile_entry)
        count += 1

    # Save the new JSON file
    new_json_path = os.path.join(f"{folder_path}/extended", "unique_variations.json")
    with open(new_json_path, 'w') as f:
        json.dump(new_json_data, f, indent=4)
    print(f"Created new JSON file with unique variations at {new_json_path}")


# Example usage
tile_set = "set4_small"
folder_path = f"data/{tile_set}"
json_path = f"data/{tile_set}/bound.json"
generate_unique_variations(folder_path, json_path)
"""
tile1_path = f"{folder_path}/extended/corner_tile_var1.png"
tile2_path = f"{folder_path}/extended/corner_tile_var4.png"
output_path = f"{folder_path}/extended/var1_vs_var4.png"
#visualize_tile_differences(tile1_path, tile2_path, output_path)
tile3_path = f"{folder_path}/extended/corner_tile_var3.png"
tile5_path = f"{folder_path}/extended/corner_tile_var5.png"
output_path = f"{folder_path}/extended/var3_vs_var5.png"
#visualize_tile_differences(tile3_path, tile5_path, output_path)
"""

