import os
import shutil
from PIL import Image, ImageChops

def is_image_equal(img1, img2):
    # Check if two images are identical
    return ImageChops.difference(img1, img2).getbbox() is None

def create_extended_folder_and_copy_tiles(folder_path):
    # Create the 'extended' folder
    extended_folder = os.path.join(folder_path, "extended")
    os.makedirs(extended_folder, exist_ok=True)

    # Copy all images to the 'extended' folder
    for file in os.listdir(folder_path):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            src = os.path.join(folder_path, file)
            dst = os.path.join(extended_folder, file)
            shutil.copy2(src, dst)
    return extended_folder

def generate_unique_variations(folder_path):
    # Create extended folder and copy tiles
    extended_folder = create_extended_folder_and_copy_tiles(folder_path)

    # Process each image in the extended folder
    for file in os.listdir(extended_folder):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(extended_folder, file)
            original = Image.open(image_path)
            variations = []

            # Generate rotated versions (90°, 180°, 270°)
            rotated = original
            for _ in range(3):
                rotated = rotated.rotate(90, expand=True)
                variations.append(rotated.copy())

            # Generate mirrored versions
            variations.append(original.transpose(Image.FLIP_LEFT_RIGHT))  # Horizontal mirror
            variations.append(original.transpose(Image.FLIP_TOP_BOTTOM))  # Vertical mirror

            # Load existing images for comparison
            existing_images = []
            for existing_file in os.listdir(extended_folder):
                if existing_file.endswith(('.png', '.jpg', '.jpeg')):
                    existing_images.append(Image.open(os.path.join(extended_folder, existing_file)))

            # Save unique variations
            count = 1
            for var in variations:
                is_unique = True

                # Compare with existing images
                for img in existing_images:
                    if is_image_equal(var, img):
                        is_unique = False
                        break

                if is_unique:
                    new_filename = f"{os.path.splitext(file)[0]}_var{count}.png"
                    var.save(os.path.join(extended_folder, new_filename))
                    print(f"Saved unique variation as {new_filename}")
                    count += 1

# Example usage
tile_set = "set2"
folder_path = f"data/{tile_set}"
generate_unique_variations(folder_path)
