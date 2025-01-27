import os
import shutil
from PIL import Image, ImageChops
import time

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

def generate_unique_variations(folder_path):
    """Generate rotated and mirrored variations of images and save only unique ones."""
    extended_folder = create_extended_folder_and_copy_tiles(folder_path)

    variations = []
    for file in os.listdir(folder_path):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, file)
            original = Image.open(image_path)
            variations.append(original)
            # Generate rotated versions (90°, 180°, 270°)
            rotated = original
            for _ in range(3):
                rotated = rotated.rotate(90, expand=True)
                variations.append(rotated.copy())

            # Generate mirrored versions
            variations.append(original.transpose(Image.FLIP_LEFT_RIGHT))  # Horizontal mirror
            variations.append(original.transpose(Image.FLIP_TOP_BOTTOM))  # Vertical mirror

    uniques = []
    for var in variations:
        is_unique = True
        for img in uniques:
            if is_image_equal(var, img):
                is_unique = False
                break
        if is_unique:
            uniques.append(var)
    count = 1
    for img in uniques:
        new_filename = f"{os.path.splitext(file)[0]}_var{count}.png"
        img.save(os.path.join(extended_folder, new_filename))
        print(f"Saved unique variation as {new_filename}")
        count += 1


# Example usage
tile_set = "set4"
folder_path = f"data/{tile_set}/comb"
tile1_path = f"{folder_path}/extended/corner_tile_var1.png"
tile2_path = f"{folder_path}/extended/corner_tile_var4.png"
output_path = f"{folder_path}/extended/var1_vs_var4.png"
#visualize_tile_differences(tile1_path, tile2_path, output_path)
tile3_path = f"{folder_path}/extended/corner_tile_var3.png"
tile5_path = f"{folder_path}/extended/corner_tile_var5.png"
output_path = f"{folder_path}/extended/var3_vs_var5.png"
#visualize_tile_differences(tile3_path, tile5_path, output_path)
generate_unique_variations(folder_path)
