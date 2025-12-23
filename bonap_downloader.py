"""
BONAP Plant Distribution Map Downloader

This module provides utilities to download plant distribution maps from the
Biota of North America Program (BONAP) website.
"""

import os
import requests
from pathlib import Path
from typing import Optional
from urllib.parse import quote


class BONAPDownloader:
    """Download plant distribution maps from BONAP."""

    BASE_URL = "https://bonap.net"
    MAP_PATH = "/MapGallery/State"

    def __init__(self, output_dir: str = "bonap_maps"):
        """
        Initialize the BONAP downloader.

        Args:
            output_dir: Directory where downloaded maps will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download_species_map(
        self,
        genus: str,
        species: str,
        filename: Optional[str] = None,
        process_colors: bool = True
    ) -> Path:
        """
        Download a distribution map for a specific plant species.

        Args:
            genus: Plant genus name (e.g., 'Asclepias')
            species: Plant species name (e.g., 'tuberosa')
            filename: Optional custom filename for the saved image.
                     If not provided, uses 'genus_species_bonap.png'
            process_colors: If True, remap colors to simplified native (green)
                          vs exotic (brown) scheme

        Returns:
            Path to the downloaded image file (processed if process_colors=True)

        Raises:
            requests.HTTPError: If the download fails
            ValueError: If genus or species are empty
        """
        if not genus or not species:
            raise ValueError("Both genus and species must be provided")

        # Capitalize genus, lowercase species (standard botanical naming)
        genus = genus.strip().capitalize()
        species = species.strip().lower()

        # Construct the image URL
        # BONAP uses "Genus species.png" format
        species_name = f"{genus} {species}"
        image_url = f"{self.BASE_URL}{self.MAP_PATH}/{species_name}.png"

        # Determine output filename
        if filename is None:
            filename = f"{genus.lower()}_{species}_bonap.png"

        output_path = self.output_dir / filename

        # Download the image
        print(f"Downloading map for {species_name}...")
        print(f"URL: {image_url}")

        response = requests.get(image_url, timeout=30)
        response.raise_for_status()

        # Save the image
        with open(output_path, 'wb') as f:
            f.write(response.content)

        print(f"✓ Map saved to: {output_path}")

        # Process colors if requested
        if process_colors:
            from bonap_processor import remap_bonap_colors
            processed_path = remap_bonap_colors(output_path)
            return processed_path

        return output_path

    def download_multiple_species(
        self,
        species_list: list[tuple[str, str]]
    ) -> dict[str, Path]:
        """
        Download maps for multiple species.

        Args:
            species_list: List of (genus, species) tuples

        Returns:
            Dictionary mapping species names to downloaded file paths
        """
        results = {}

        for genus, species in species_list:
            try:
                species_key = f"{genus} {species}"
                path = self.download_species_map(genus, species)
                results[species_key] = path
            except Exception as e:
                print(f"✗ Failed to download {genus} {species}: {e}")
                results[species_key] = None

        return results


def download_plant_map(genus: str, species: str, output_dir: str = "bonap_maps", process_colors: bool = True) -> Path:
    """
    Convenience function to download a single plant distribution map.

    Args:
        genus: Plant genus name
        species: Plant species name
        output_dir: Directory where the map will be saved
        process_colors: If True, remap colors to simplified native (green)
                       vs exotic (brown) scheme

    Returns:
        Path to the downloaded image file
    """
    downloader = BONAPDownloader(output_dir)
    return downloader.download_species_map(genus, species, process_colors=process_colors)
