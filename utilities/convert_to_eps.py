"""
Convert PNG to EPS for LaTeX IEEE Paper
This script converts the dashboard screenshot from PNG to EPS format
"""

from PIL import Image
import os

def convert_png_to_eps():
    """Convert dashboard screenshot from PNG to EPS format"""
    
    # Paths
    png_path = r"d:\OneDrive_Personal\OneDrive\My Research\01_Working\Drones\SimulationSystem\IEEE_Paper_Coverage_First_2025\Coverage_First_Study_20250822_193758\Figures\PNG\dashboard_screenshot.png"
    eps_path = r"d:\OneDrive_Personal\OneDrive\My Research\01_Working\Drones\SimulationSystem\IEEE_Paper_Coverage_First_2025\Coverage_First_Study_20250822_193758\Figures\EPS\dashboard_screenshot.eps"
    
    try:
        # Open the PNG image
        img = Image.open(png_path)
        
        # Convert to RGB if necessary (EPS doesn't support RGBA)
        if img.mode in ('RGBA', 'LA'):
            # Create a white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
            else:
                background.paste(img)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Save as EPS
        img.save(eps_path, 'EPS')
        
        print("✅ Conversion successful!")
        print(f"📁 PNG file: {png_path}")
        print(f"📁 EPS file: {eps_path}")
        print(f"📏 Image size: {img.size}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False

if __name__ == "__main__":
    print("Dashboard Screenshot PNG to EPS Converter")
    print("=" * 50)
    convert_png_to_eps()
