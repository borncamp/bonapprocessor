   # Extract just the filename without path
    filename=$1

    # Create output filename (remove _processed suffix and add _with_legend)
    base_name="${filename%_processed.png}"
    output_file="./${base_name}_with_legend.png"

    echo "Input File: $1"
    echo "base_name: $base_name"
    echo "output_file: $output_file"

    echo "Processing: $filename"

    # Run Python to add legend
    python3 -c "
from add_legend import add_legend_to_map
from pathlib import Path

try:
    add_legend_to_map('$filename', Path('$output_file'))
    print('✓ Saved to: $output_file')
except Exception as e:
    print(f'✗ Error: {e}')
    exit(1)
" 