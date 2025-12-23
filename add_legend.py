#!/usr/bin/env python3
"""
Add a legend/key to processed BONAP maps.
Displays the color classifications on the left side of the image.
"""

from pathlib import Path
from typing import Optional, Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# Color definitions (matching bonap_processor.py)
NATIVE_COLOR = (34, 139, 34)      # Forest green
NON_NATIVE_COLOR = (139, 69, 19)  # Saddle brown
NOXIOUS_COLOR = (139, 69, 19)     # Saddle brown (same as non-native)
NOT_PRESENT_COLOR = (173, 142, 0)  # Olive/mustard


def add_legend_to_map(
    input_path: Path,
    output_path: Optional[Path] = None,
    legend_width: int = 150,
    background_color: Tuple[int, int, int] = (255, 255, 255)
) -> Path:
    """
    Add a legend to a processed BONAP map.

    Args:
        input_path: Path to the processed BONAP map image
        output_path: Path for the output image. If None, adds '_with_legend' to filename
        legend_width: Width of the legend area in pixels
        background_color: RGB color for legend background

    Returns:
        Path to the image with legend
    """
    # Ensure input_path is a Path object
    input_path = Path(input_path)

    # Load the processed map
    map_img = Image.open(input_path)
    map_width, map_height = map_img.size

    # Create new image with space for legend on the left
    total_width = legend_width + map_width
    new_img = Image.new('RGB', (total_width, map_height), background_color)

    # Paste the map on the right side
    new_img.paste(map_img, (legend_width, 0))

    # Draw legend on the left side
    draw = ImageDraw.Draw(new_img)

    # Try to use a better font, fall back to default if not available
    try:
        # Try common font locations
        font_size = 14
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "C:\\Windows\\Fonts\\arial.ttf",  # Windows
        ]
        font = None
        for font_path in font_paths:
            if Path(font_path).exists():
                font = ImageFont.truetype(font_path, font_size)
                break
        if font is None:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # Calculate vertical spacing
    color_box_size = 20
    padding = 15
    line_height = 30
    start_y = 40

    # Title
    title_text = "Legend"
    draw.text((padding, 10), title_text, fill=(0, 0, 0), font=font)

    # Draw legend items
    legend_items = [
        ("Native", NATIVE_COLOR),
        ("Non-Native", NOT_PRESENT_COLOR),
        ("Noxious", NON_NATIVE_COLOR),
    ]

    y_position = start_y
    for label, color in legend_items:
        # Draw color box
        box_x1 = padding
        box_y1 = y_position
        box_x2 = padding + color_box_size
        box_y2 = y_position + color_box_size

        draw.rectangle([box_x1, box_y1, box_x2, box_y2], fill=color, outline=(0, 0, 0))

        # Draw label
        text_x = padding + color_box_size + 10
        text_y = y_position + (color_box_size // 2) - 7  # Center text vertically

        draw.text((text_x, text_y), label, fill=(0, 0, 0), font=font)

        y_position += line_height

    # Determine output path
    if output_path is None:
        stem = input_path.stem
        suffix = input_path.suffix
        output_path = input_path.parent / f"{stem}_with_legend{suffix}"

    # Save the image
    new_img.save(output_path)

    print(f"✓ Added legend to: {output_path}")

    return output_path


def add_legend_to_processed_map(
    genus: str,
    species: str,
    input_dir: str = "bonap_maps",
    output_dir: Optional[str] = None
) -> Path:
    """
    Add legend to a processed BONAP map by genus and species name.

    Args:
        genus: Plant genus name
        species: Plant species name
        input_dir: Directory containing the processed map
        output_dir: Directory for output. If None, uses input_dir

    Returns:
        Path to the image with legend
    """
    # Construct input filename based on naming convention
    filename = f"{genus.lower()}_{species.lower()}_bonap_processed.png"
    input_path = Path(input_dir) / filename

    if not input_path.exists():
        raise FileNotFoundError(f"Processed map not found: {input_path}")

    # Construct output path
    if output_dir:
        output_filename = f"{genus.lower()}_{species.lower()}_bonap_processed_with_legend.png"
        output_path = Path(output_dir) / output_filename
    else:
        output_path = None  # Will use default naming in same directory

    return add_legend_to_map(input_path, output_path)


if __name__ == "__main__":
    # Example: Add legend to Asclepias tuberosa processed map
    add_legend_to_processed_map("Asclepias", "tuberosa")
