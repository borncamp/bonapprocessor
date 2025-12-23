#!/usr/bin/env python3
"""
Download BONAP maps for all species in the Shopify CSV export.
"""

from bonap_downloader import BONAPDownloader
from parse_scientific_names import parse_csv_scientific_names


def main():
    """Download BONAP maps for all species in the CSV."""
    csv_file = "plugs.csv"

    print("Parsing scientific names from CSV...")
    try:
        scientific_names = parse_csv_scientific_names(csv_file)
        print(f"Found {len(scientific_names)} unique species\n")
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return

    # Initialize downloader
    downloader = BONAPDownloader(output_dir="bonap_maps")

    # Download maps for all species
    print("Downloading BONAP maps...\n")
    results = downloader.download_multiple_species(scientific_names)

    # Print summary
    print("\n" + "=" * 60)
    print("Download Summary")
    print("=" * 60)

    successful = sum(1 for path in results.values() if path is not None)
    failed = len(results) - successful

    print(f"\nTotal species: {len(results)}")
    print(f"✓ Successfully downloaded: {successful}")
    print(f"✗ Failed: {failed}")

    if failed > 0:
        print("\nFailed downloads:")
        for species_name, path in results.items():
            if path is None:
                print(f"  - {species_name}")


if __name__ == "__main__":
    main()
