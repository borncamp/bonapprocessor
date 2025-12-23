# BONAP Plant Distribution Map Downloader

A Python utility to download plant distribution maps from the [Biota of North America Program (BONAP)](https://bonap.net/) website.

## Overview

BONAP provides detailed distribution maps for North American plant species. This tool allows you to easily download these maps programmatically by providing the genus and species name.

## Installation

1. Clone or download this project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

```python
from bonap_downloader import download_plant_map

# Download a map for Asclepias tuberosa (Butterfly milkweed)
path = download_plant_map("Asclepias", "tuberosa")
print(f"Map saved to: {path}")
```

### Using the BONAPDownloader Class

```python
from bonap_downloader import BONAPDownloader

# Initialize downloader with custom output directory
downloader = BONAPDownloader(output_dir="my_maps")

# Download a single species
path = downloader.download_species_map("Asclepias", "tuberosa")

# Download with custom filename
path = downloader.download_species_map(
    "Quercus",
    "alba",
    filename="white_oak.png"
)
```

### Download Multiple Species

```python
from bonap_downloader import BONAPDownloader

downloader = BONAPDownloader(output_dir="bonap_maps")

species_list = [
    ("Asclepias", "tuberosa"),
    ("Asclepias", "incarnata"),
    ("Quercus", "alba"),
    ("Acer", "rubrum"),
]

results = downloader.download_multiple_species(species_list)

for species_name, path in results.items():
    if path:
        print(f"Downloaded: {species_name}")
```

## Examples

Run the example script to see the downloader in action:

```bash
python example.py
```

## How It Works

BONAP organizes plant maps by genus. For example, maps for the genus *Asclepias* are listed at:
```
https://bonap.net/Napa/TaxonMaps/Genus/State/Asclepias
```

Individual species maps follow the pattern:
```
https://bonap.net/MapGallery/State/Genus species.png
```

This tool constructs the appropriate URL based on the genus and species you provide, then downloads the PNG image.

## API Reference

### `download_plant_map(genus, species, output_dir="bonap_maps")`

Convenience function to download a single plant distribution map.

**Parameters:**
- `genus` (str): Plant genus name (e.g., "Asclepias")
- `species` (str): Plant species name (e.g., "tuberosa")
- `output_dir` (str): Directory where the map will be saved (default: "bonap_maps")

**Returns:**
- `Path`: Path to the downloaded image file

### `BONAPDownloader` Class

#### `__init__(output_dir="bonap_maps")`

Initialize the downloader.

**Parameters:**
- `output_dir` (str): Directory where downloaded maps will be saved

#### `download_species_map(genus, species, filename=None)`

Download a distribution map for a specific plant species.

**Parameters:**
- `genus` (str): Plant genus name
- `species` (str): Plant species name
- `filename` (str, optional): Custom filename for the saved image

**Returns:**
- `Path`: Path to the downloaded image file

**Raises:**
- `requests.HTTPError`: If the download fails
- `ValueError`: If genus or species are empty

#### `download_multiple_species(species_list)`

Download maps for multiple species.

**Parameters:**
- `species_list` (list): List of (genus, species) tuples

**Returns:**
- `dict`: Dictionary mapping species names to downloaded file paths

## Notes

- The genus name will be automatically capitalized
- The species name will be automatically converted to lowercase
- Downloaded files are saved as `Genus_species.png` by default
- If a species map doesn't exist on BONAP, the download will fail with an HTTP error

## License

This is a utility tool for accessing publicly available data from BONAP. Please respect BONAP's terms of use and cite their work appropriately when using these maps.

## Credits

Plant distribution data courtesy of the [Biota of North America Program (BONAP)](https://bonap.net/).
