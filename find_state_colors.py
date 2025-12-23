#!/usr/bin/env python3
"""Find actual state fill colors (excluding background, borders, text)."""

import numpy as np
from PIL import Image
from collections import Counter

def find_state_colors(image_path):
    """Find colors that are likely state fills."""
    img = Image.open(image_path)
    arr = np.array(img)[:, :, :3]

    # Get all pixels
    pixels = arr.reshape(-1, 3)
    pixel_tuples = [tuple(p) for p in pixels]
    color_counts = Counter(pixel_tuples)

    # Background/border colors to ignore
    ignore_colors = {
        (153, 204, 255),  # Light blue background
        (149, 205, 252),  # Light blue variant
        (100, 200, 250),  # Light blue variant
        (0, 0, 0),        # Black borders
        (169, 169, 169),  # Gray (Mexico)
    }

    print("State/Province fill colors (excluding background/borders):\n")
    for color, count in color_counts.most_common(30):
        if color not in ignore_colors and count > 500:
            percentage = (count / len(pixel_tuples)) * 100
            print(f"RGB{color} - {count:6d} pixels ({percentage:5.2f}%)")

if __name__ == "__main__":
    find_state_colors("bonap_maps/asclepias_tuberosa_bonap.png")
