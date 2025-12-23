#!/usr/bin/env bash
"""
Batch add legends to all processed BONAP maps.
Processes all *_processed.png files in bonap_maps/ and saves them with legends to with_key/
"""

# Create output directory if it doesn't exist
mkdir -p with_key

# Counter for tracking progress
total=0
processed=0
failed=0

# Count total files
total=$(find bonap_maps -name "*_processed.png" -type f | wc -l | tr -d ' ')

echo "Found $total processed maps to add legends to"
echo ""

# Process each processed map
for map_file in bonap_maps/*_processed.png; do
    # Skip if no files match
    if [ ! -f "$map_file" ]; then
        echo "No processed maps found in bonap_maps/"
        exit 0
    fi

    # Extract just the filename without path
    filename=$(basename "$map_file")

    # Create output filename (remove _processed suffix and add _with_legend)
    base_name="${filename%_processed.png}"
    output_file="with_key/${base_name}_with_legend.png"

    echo "Processing: $filename"

    # Run Python to add legend
    python3 -c "
from add_legend import add_legend_to_map
from pathlib import Path

try:
    add_legend_to_map('$map_file', Path('$output_file'))
    print('✓ Saved to: $output_file')
except Exception as e:
    print(f'✗ Error: {e}')
    exit(1)
" && ((processed++)) || ((failed++))

    echo ""
done

# Print summary
echo "========================================"
echo "Batch Processing Summary"
echo "========================================"
echo "Total files: $total"
echo "✓ Successfully processed: $processed"
echo "✗ Failed: $failed"
echo ""
echo "Output directory: with_key/"
