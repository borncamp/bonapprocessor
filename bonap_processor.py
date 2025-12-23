"""
BONAP Image Processor

This module provides utilities to process BONAP distribution maps,
simplifying the color scheme to make native vs. exotic status clearer.
"""

from pathlib import Path
from typing import Optional, Tuple
import numpy as np
from PIL import Image


# BONAP color definitions (actual RGB values from maps)
# Based on official BONAP color key at bonap.org/MapKey.html

# These colors indicate NATIVE status (species naturally occurs in this region)
NATIVE_COLORS = [
    (0, 128, 0),      # Dark green - species present and native
    (255, 255, 0),    # Yellow - species present and rare (native but rare)
    (255, 165, 0),    # Orange - species extirpated/historic (was native)
    (0, 255, 0),      # Light/bright green - species present and not rare
    (0, 221, 145),    # Cyan/turquoise - species native but adventive in state (still native)
    (0, 165, 108),    # Teal - questionable presence / adventive variant (treat as native)
]

# Colors to leave unchanged (neither native nor exotic - species not present)
# (173, 142, 0) - Olive/mustard - species NOT present in state

# These colors indicate EXOTIC/NON-NATIVE status (human-introduced, not native to region)
EXOTIC_COLORS = [
    (255, 0, 255),    # Magenta - species noxious (truly exotic)
    (0, 0, 255),      # Blue - species present and exotic
    (135, 206, 235),  # Sky blue - species waif
]

# Target colors for remapping
TARGET_NATIVE_COLOR = (34, 139, 34)    # Forest green
TARGET_EXOTIC_COLOR = (139, 69, 19)    # Saddle brown


def color_distance(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
    """
    Calculate Euclidean distance between two RGB colors.

    Args:
        color1: First RGB color tuple
        color2: Second RGB color tuple

    Returns:
        Distance between the two colors
    """
    return np.sqrt(sum((int(c1) - int(c2)) ** 2 for c1, c2 in zip(color1, color2)))


def is_native_color(pixel: Tuple[int, int, int], threshold: float = 5.0) -> Optional[bool]:
    """
    Determine if a pixel color represents native or exotic status.

    Args:
        pixel: RGB color tuple
        threshold: Maximum color distance to consider a match (default 5 for exact matching)

    Returns:
        True if native, False if exotic, None if neither (e.g., background/text)
    """
    # Check if it's close to any native color
    for native_color in NATIVE_COLORS:
        if color_distance(pixel, native_color) < threshold:
            return True

    # Check if it's close to any exotic color
    for exotic_color in EXOTIC_COLORS:
        if color_distance(pixel, exotic_color) < threshold:
            return False

    # Not close to any defined color (probably background, text, or border)
    return None


def remap_bonap_colors(
    input_path: Path,
    output_path: Optional[Path] = None,
    native_color: Tuple[int, int, int] = TARGET_NATIVE_COLOR,
    exotic_color: Tuple[int, int, int] = TARGET_EXOTIC_COLOR,
    threshold: float = 5.0
) -> Path:
    """
    Remap BONAP map colors to a simpler native (green) vs exotic (brown) scheme.

    Args:
        input_path: Path to the input BONAP map image
        output_path: Path for the output image. If None, adds '_processed' to filename
        native_color: RGB color to use for native status
        exotic_color: RGB color to use for exotic status
        threshold: Color distance threshold for matching

    Returns:
        Path to the processed image
    """
    # Ensure input_path is a Path object
    input_path = Path(input_path)

    # Load image
    img = Image.open(input_path)
    img_array = np.array(img)

    # Create output array
    output_array = img_array.copy()

    # Process each pixel
    height, width = img_array.shape[:2]
    pixels_processed = 0
    native_count = 0
    exotic_count = 0

    for y in range(height):
        for x in range(width):
            pixel = tuple(img_array[y, x][:3])  # Get RGB, ignore alpha if present

            status = is_native_color(pixel, threshold)

            if status is True:  # Native
                output_array[y, x][:3] = native_color
                native_count += 1
                pixels_processed += 1
            elif status is False:  # Exotic
                output_array[y, x][:3] = exotic_color
                exotic_count += 1
                pixels_processed += 1
            # If None, leave the pixel unchanged (background, text, borders)

    # Note: Diagonal hatching removal disabled - minimal visual impact and avoids processing time

    # Crop to focus on continental US area (removes most of Canada, Alaska, and ocean)
    # Based on the pink box in the reference image, crop to the continental US
    # - Top: Just above US-Canada border (around 50% down)
    # - Bottom: Extended to include more southern area (around 100%)
    # - Left: West coast of US, cropped 10% more (around 33% right)
    # - Right: East coast of US, cropped 10% more (around 73% right)
    crop_top = int(height * 0.50)  # Start just above US-Canada border
    crop_bottom = int(height * 1.00)  # End at full bottom (extended 5%)
    crop_left = int(width * 0.33)  # Start at west coast (cropped 10% more)
    crop_right = int(width * 0.73)  # End at east coast (cropped 10% more)

    output_array = output_array[crop_top:crop_bottom, crop_left:crop_right]
    print(f"✓ Cropped to {output_array.shape[1]}x{output_array.shape[0]} (focused on continental US)")

    # Determine output path
    if output_path is None:
        stem = input_path.stem
        suffix = input_path.suffix
        output_path = input_path.parent / f"{stem}_processed{suffix}"

    # Save processed image
    output_img = Image.fromarray(output_array)
    output_img.save(output_path)

    print(f"✓ Processed {pixels_processed} pixels ({native_count} native, {exotic_count} exotic)")
    print(f"✓ Saved to: {output_path}")

    return output_path


def process_bonap_map(
    genus: str,
    species: str,
    input_dir: str = "bonap_maps",
    output_dir: Optional[str] = None
) -> Path:
    """
    Process a downloaded BONAP map by genus and species name.

    Args:
        genus: Plant genus name
        species: Plant species name
        input_dir: Directory containing the downloaded map
        output_dir: Directory for processed output. If None, uses input_dir

    Returns:
        Path to the processed image
    """
    # Construct input filename based on bonap_downloader naming convention
    filename = f"{genus.lower()}_{species.lower()}_bonap.png"
    input_path = Path(input_dir) / filename

    if not input_path.exists():
        raise FileNotFoundError(f"Map not found: {input_path}")

    # Construct output path
    if output_dir:
        output_path = Path(output_dir) / f"{genus.lower()}_{species.lower()}_bonap_processed.png"
    else:
        output_path = None  # Will use default naming in same directory

    return remap_bonap_colors(input_path, output_path)
