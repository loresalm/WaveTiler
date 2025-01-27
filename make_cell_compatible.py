from PIL import Image
import numpy as np
"""
def make_tiles_compatible(img1_path, direction, img2_path, output1_path, output2_path):
    # Load images and convert to numpy arrays
    img1 = Image.open(img1_path).convert('RGB')
    img2 = Image.open(img2_path).convert('RGB')

    img1_array = np.array(img1)
    img2_array = np.array(img2)

    if direction == "left":
        # Left of img1 (column 0), Right of img2 (last column)
        # avg_values = (img1_array[:, 0, :] + img2_array[:, -1, :]) // 2
        img1_array[:, 0, :] = img1_array[:, 0, :]  # Update leftmost column of img1
        img2_array[:, -1, :] = img1_array[:, 0, :]  # Update rightmost column of img2

    elif direction == "right":
        # Right of img1 (last column), Left of img2 (column 0)
        # avg_values = (img1_array[:, -1, :] + img2_array[:, 0, :]) // 2
        img1_array[:, -1, :] = img1_array[:, -1, :]  # Update rightmost column of img1
        img2_array[:, 0, :] = img1_array[:, -1, :]  # Update leftmost column of img2

    elif direction == "top":
        # Top of img1 (row 0), Bottom of img2 (last row)
        # avg_values = (img1_array[0, :, :] + img2_array[-1, :, :]) // 2
        img1_array[0, :, :] = img1_array[0, :, :]  # Update top row of img1
        img2_array[-1, :, :] = img1_array[0, :, :]  # Update bottom row of img2

    elif direction == "bottom":
        # Bottom of img1 (last row), Top of img2 (row 0)
        # avg_values = (img1_array[-1, :, :] + img2_array[0, :, :]) // 2
        img1_array[-1, :, :] = img1_array[-1, :, :]  # Update bottom row of img1
        img2_array[0, :, :] = img1_array[-1, :, :]  # Update top row of img2

    else:
        raise ValueError("Invalid direction. Choose from 'left', 'right', 'top', 'bottom'.")

    # Save the updated images
    Image.fromarray(img1_array).save(output1_path)
    Image.fromarray(img2_array).save(output2_path)

    print(f"Updated images saved as {output1_path} and {output2_path}")
"""

# Example usage
start_path = "data/set4/start.png"
start_img = Image.open(start_path).convert('RGB')
start = np.array(start_img)

stop_path = "data/set4/stop.png"
stop_img = Image.open(stop_path).convert('RGB')
stop = np.array(stop_img)

leg1_long_path = "data/set4/1leg_long.png"
leg1_long_img = Image.open(leg1_long_path).convert('RGB')
leg1_long = np.array(leg1_long_img)

leg2_long_path = "data/set4/2leg_long.png"
leg2_long_img = Image.open(leg2_long_path).convert('RGB')
leg2_long = np.array(leg2_long_img)

leg0_long_path = "data/set4/0leg_long.png"
leg0_long_img = Image.open(leg0_long_path).convert('RGB')
leg0_long = np.array(leg0_long_img)

leg1_corner_path = "data/set4/1leg_corner.png"
leg1_corner_img = Image.open(leg1_corner_path).convert('RGB')
leg1_corner = np.array(leg1_corner_img)

leg2_corner_path = "data/set4/2leg_corner.png"
leg2_corner_img = Image.open(leg2_corner_path).convert('RGB')
leg2_corner = np.array(leg2_corner_img)

leg1_long[:, 0, :] = leg1_long[:, 0, :]
leg1_long[:, -1, :] = leg1_long[:, 0, :]

leg2_long[:, 0, :] = leg1_long[:, 0, :]
leg2_long[:, -1, :] = leg1_long[:, 0, :]

leg0_long[:, 0, :] = leg1_long[:, 0, :]
leg0_long[:, -1, :] = leg1_long[:, 0, :]

leg1_corner[:, 0, :] = leg1_long[:, 0, :]
leg1_corner[0, :, :] = leg1_long[:, 0, :]

leg2_corner[:, 0, :] = leg1_long[:, 0, :]
leg2_corner[0, :, :] = leg1_long[:, 0, :]


start[:, -1, :] = leg1_long[:, 0, :]
stop[:, 0, :] = leg1_long[:, 0, :]


leg1_long_path = "data/set4/comb/leg1_long.png"
leg2_long_path = "data/set4/comb/leg2_long.png"
leg0_long_path = "data/set4/comb/leg0_long.png"
leg1_corner_path = "data/set4/comb/leg1_corner.png"
leg_2_corner_path = "data/set4/comb/leg2_corner.png"
start_path = "data/set4/comb/start.png"
stop_path = "data/set4/comb/stop.png"

Image.fromarray(leg1_long).save(leg1_long_path)
Image.fromarray(leg2_long).save(leg2_long_path)
Image.fromarray(leg0_long).save(leg0_long_path)
Image.fromarray(leg1_corner).save(leg1_corner_path)
Image.fromarray(leg2_corner).save(leg2_corner_path)
Image.fromarray(start).save(start_path)
Image.fromarray(stop).save(stop_path)

"""
img2 = "data/set4/body.png"
out_img1 = "data/set4/comb/comb_head.png"
out_img2 = "data/set4/comb/comb_body.png"
make_tiles_compatible(img1, "right", img2, out_img1, out_img2)

img1 = "data/set4/comb/comb_body.png"
img2 = "data/set4/tail.png"
out_img1 = "data/set4/comb/comb_body.png"
out_img2 = "data/set4/comb/comb_tail.png"
make_tiles_compatible(img1, "right", img2, out_img1, out_img2)


img1 = "data/set4/corner.png"
img2 = "data/set4/tail_corner.png"
out_img1 = "data/set4/comb/comb_corner.png"
out_img2 = "data/set4/comb/comb_tail_corner.png"
make_tiles_compatible(img1, "top", img2, out_img1, out_img2)

img1 = "data/set4/comb/comb_corner.png"
img2 = "data/set4/head_corner.png"
out_img1 = "data/set4/comb/comb_corner.png"
out_img2 = "data/set4/comb/head_corner.png"
make_tiles_compatible(img1, "left", img2, out_img1, out_img2)
"""
