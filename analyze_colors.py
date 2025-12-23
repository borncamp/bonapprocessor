#!/usr/bin/env python3
"""Analyze the actual colors used in a BONAP map."""

import numpy as np
from PIL import Image
from collections import Counter
from pathlib import Path

def analyze_bonap_colors(image_path):
    """Analyze and display the most common colors in a BONAP map."""
    img = Image.open(image_path)
    img_array = np.array(img)

    # Get just RGB channels
    if img_array.shape[2] == 4:  # Has alpha channel
        rgb_array = img_array[:, :, :3]
    else:
        rgb_array = img_array

    # Reshape to list of RGB tuples
    height, width = rgb_array.shape[:2]
    pixels = rgb_array.reshape(-1, 3)

    # Convert to list of tuples
    pixel_tuples = [tuple(p) for p in pixels]

    # Count occurrences
    color_counts = Counter(pixel_tuples)

    # Get most common colors
    print(f"\nAnalyzing: {image_path}")
    print(f"Image size: {width}x{height}")
    print(f"\nTop 20 most common colors (RGB):\n")

    for i, (color, count) in enumerate(color_counts.most_common(20), 1):
        percentage = (count / len(pixel_tuples)) * 100
        print(f"{i:2d}. RGB{color} - {count:6d} pixels ({percentage:5.2f}%)")

    return color_counts

if __name__ == "__main__":
    analyze_bonap_colors("bonap_maps/asclepias_tuberosa_bonap.png")
