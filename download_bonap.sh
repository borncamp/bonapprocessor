#!/usr/bin/env bash
#
# BONAP Plant Map Downloader Script
#
# Usage: bash download_bonap.sh <genus> <species>
# Example: bash download_bonap.sh Asclepias tuberosa
#

# Check if correct number of arguments provided
if [ $# -ne 2 ]; then
    echo "Usage: bash $0 <genus> <species>"
    echo "Example: bash $0 Asclepias tuberosa"
    exit 1
fi

GENUS="$1"
SPECIES="$2"

# Run the Python downloader
python3 -c "
from bonap_downloader import download_plant_map
download_plant_map('$GENUS', '$SPECIES')
"
