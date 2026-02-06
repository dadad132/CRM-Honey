"""Generate app icons for PWA"""
from PIL import Image, ImageDraw
import os

# Icon sizes needed for PWA
sizes = [72, 96, 128, 144, 152, 192, 384, 512]

# Output directory
output_dir = r"c:\Users\admin\Documents\TempFiles\cem-backend\app\static\icons"

def create_icon(size):
    """Create a simple app icon with gradient background and shield"""
    # Create image with RGBA
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background - rounded rectangle (simulated with circle corners)
    corner_radius = size // 5
    
    # Draw rounded rectangle background
    # Main rectangle
    draw.rectangle([corner_radius, 0, size - corner_radius, size], fill='#DC2626')
    draw.rectangle([0, corner_radius, size, size - corner_radius], fill='#DC2626')
    
    # Corner circles
    draw.ellipse([0, 0, corner_radius * 2, corner_radius * 2], fill='#DC2626')
    draw.ellipse([size - corner_radius * 2, 0, size, corner_radius * 2], fill='#DC2626')
    draw.ellipse([0, size - corner_radius * 2, corner_radius * 2, size], fill='#DC2626')
    draw.ellipse([size - corner_radius * 2, size - corner_radius * 2, size, size], fill='#DC2626')
    
    # Draw shield icon in the center
    center_x = size // 2
    center_y = size // 2
    shield_size = int(size * 0.5)
    
    # Shield outline (white)
    shield_points = [
        (center_x, center_y - shield_size // 2),  # Top
        (center_x + shield_size // 2, center_y - shield_size // 4),  # Top right
        (center_x + shield_size // 2, center_y + shield_size // 6),  # Right
        (center_x, center_y + shield_size // 2),  # Bottom
        (center_x - shield_size // 2, center_y + shield_size // 6),  # Left
        (center_x - shield_size // 2, center_y - shield_size // 4),  # Top left
    ]
    draw.polygon(shield_points, fill='white')
    
    # Inner shield (smaller, red)
    inner_size = int(shield_size * 0.7)
    inner_points = [
        (center_x, center_y - inner_size // 2),
        (center_x + inner_size // 2, center_y - inner_size // 4),
        (center_x + inner_size // 2, center_y + inner_size // 6),
        (center_x, center_y + inner_size // 2),
        (center_x - inner_size // 2, center_y + inner_size // 6),
        (center_x - inner_size // 2, center_y - inner_size // 4),
    ]
    draw.polygon(inner_points, fill='#991B1B')
    
    return img

# Generate all sizes
for size in sizes:
    icon = create_icon(size)
    filename = os.path.join(output_dir, f"icon-{size}x{size}.png")
    icon.save(filename, 'PNG')
    print(f"Created {filename}")

print("\nAll icons generated successfully!")
