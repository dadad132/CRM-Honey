# Icon generation script
# Run this script to generate PNG icons from the SVG

# You can use this online tool: https://realfavicongenerator.net/
# Or install Python pillow and cairosvg:
# pip install pillow cairosvg

# Then run:
"""
import cairosvg
from PIL import Image
import io

sizes = [72, 96, 128, 144, 152, 192, 384, 512]

for size in sizes:
    # Convert SVG to PNG
    png_data = cairosvg.svg2png(
        url='icon.svg',
        output_width=size,
        output_height=size
    )
    
    # Save the PNG
    with open(f'icon-{size}x{size}.png', 'wb') as f:
        f.write(png_data)
    
    print(f'Created icon-{size}x{size}.png')
"""

# For now, you can use any PNG icon generator tool
# Just make sure to create these files:
# - icon-72x72.png
# - icon-96x96.png
# - icon-128x128.png
# - icon-144x144.png
# - icon-152x152.png
# - icon-192x192.png
# - icon-384x384.png
# - icon-512x512.png
