#!/usr/bin/env python3
"""
Parse scientific names from Shopify CSV export.
Extracts scientific names (genus species) from the Title column.
"""

import csv
import re
from pathlib import Path
from typing import List, Tuple


def extract_scientific_name(title: str) -> str | None:
    """
    Extract scientific name from a title string.

    Format: "Common Name - Genus species - Size"
    Returns: "Genus species" or None if not found

    Args:
        title: Product title string

    Returns:
        Scientific name (genus species) or None
    """
    # Match text between two dashes
    # Pattern: anything - (scientific name) - anything
    pattern = r'-\s*([A-Z][a-z]+\s+[a-z]+)\s*-'

    match = re.search(pattern, title)
    if match:
        return match.group(1).strip()

    return None


def parse_csv_scientific_names(csv_path: str) -> List[Tuple[str, str]]:
    """
    Parse scientific names from Shopify CSV export.

    Args:
        csv_path: Path to the CSV file

    Returns:
        List of (genus, species) tuples
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    scientific_names = []
    seen = set()  # Track duplicates

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            title = row.get('Title', '')

            if not title:
                continue

            scientific_name = extract_scientific_name(title)

            if scientific_name:
                # Split into genus and species
                parts = scientific_name.split()
                if len(parts) == 2:
                    genus, species = parts

                    # Track unique names
                    key = f"{genus} {species}"
                    if key not in seen:
                        scientific_names.append((genus, species))
                        seen.add(key)

    return scientific_names


def main():
    """Main function to parse and display scientific names."""
    csv_file = "plugs.csv"

    try:
        scientific_names = parse_csv_scientific_names(csv_file)

        print(f"Found {len(scientific_names)} unique scientific names:\n")

        for genus, species in sorted(scientific_names):
            print(f"{genus} {species}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
