#!/usr/bin/env python3
"""
Example usage of the BONAP downloader utility.
"""

from bonap_downloader import BONAPDownloader, download_plant_map
from bonap_processor import process_bonap_map


def example_single_download():
    """Download a single species map."""
    print("=== Example 1: Download single species ===\n")

    # Simple usage with convenience function
    path = download_plant_map("Asclepias", "tuberosa")
    print(f"\nDownloaded to: {path}\n")


def example_download_with_processing():
    """Download and automatically process colors."""
    print("=== Example 2: Download with color processing ===\n")

    # Download and process in one step
    path = download_plant_map("Asclepias", "tuberosa", process_colors=True)
    print(f"\nProcessed map saved to: {path}\n")


def example_process_existing():
    """Process an already downloaded map."""
    print("=== Example 3: Process existing map ===\n")

    # First download the map
    print("Downloading original map...")
    download_plant_map("Quercus", "alba")

    # Then process it separately
    print("\nProcessing colors...")
    processed_path = process_bonap_map("Quercus", "alba")
    print(f"\nProcessed map saved to: {processed_path}\n")


def example_multiple_downloads():
    """Download multiple species maps."""
    print("=== Example 4: Download multiple species ===\n")

    downloader = BONAPDownloader(output_dir="bonap_maps")

    # List of species to download
    species_list = [
        ("Asclepias", "tuberosa"),      # Butterfly milkweed
        ("Asclepias", "incarnata"),     # Swamp milkweed
        ("Asclepias", "syriaca"),       # Common milkweed
        ("Quercus", "alba"),            # White oak
        ("Acer", "rubrum"),             # Red maple
    ]

    results = downloader.download_multiple_species(species_list)

    print("\n=== Download Summary ===")
    for species_name, path in results.items():
        if path:
            print(f"✓ {species_name}: {path}")
        else:
            print(f"✗ {species_name}: Failed")


def example_custom_output():
    """Download with custom output directory and filename."""
    print("\n=== Example 5: Custom output settings ===\n")

    downloader = BONAPDownloader(output_dir="my_plants")
    path = downloader.download_species_map(
        "Asclepias",
        "tuberosa",
        filename="butterfly_milkweed.png"
    )
    print(f"\nDownloaded to: {path}\n")


if __name__ == "__main__":
    # Run example 1: Download Asclepias tuberosa
    example_single_download()

    # Uncomment to run other examples:
    # example_download_with_processing()
    # example_process_existing()
    # example_multiple_downloads()
    # example_custom_output()
