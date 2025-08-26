"""
Dashboard Screenshot Capture Script
This script will help capture the dashboard screenshot from the running application
"""

import os
import time
from PIL import ImageGrab
import subprocess

def capture_dashboard_screenshot():
    """
    Capture dashboard screenshot from browser
    """
    # Path for saving the screenshot
    base_path = r"d:\OneDrive_Personal\OneDrive\My Research\01_Working\Drones\SimulationSystem\IEEE_Paper_Coverage_First_2025\Coverage_First_Study_20250822_193758\Figures"
    png_path = os.path.join(base_path, "PNG", "dashboard_screenshot.png")
    
    print("Dashboard Screenshot Capture Tool")
    print("=" * 50)
    print("Instructions:")
    print("1. Make sure your dashboard is running at http://localhost:8050")
    print("2. Open the dashboard in your browser")
    print("3. Ensure the dashboard shows PSO optimization results")
    print("4. Press ENTER when ready to capture...")
    
    input("Press ENTER when your dashboard is ready for screenshot...")
    
    print("Capturing screenshot in 3 seconds...")
    time.sleep(3)
    
    # Capture full screen
    screenshot = ImageGrab.grab()
    
    # Save the screenshot
    screenshot.save(png_path)
    print(f"Screenshot saved to: {png_path}")
    
    # Also save to EPS folder (as PNG for now, convert to EPS later)
    eps_folder = os.path.join(base_path, "EPS")
    eps_path = os.path.join(eps_folder, "dashboard_screenshot.png")
    screenshot.save(eps_path)
    print(f"Also saved to: {eps_path}")
    
    print("\nScreenshot capture completed!")
    print("The image has been saved to both PNG and EPS folders.")
    print("You may want to crop the image to show only the dashboard area.")

if __name__ == "__main__":
    capture_dashboard_screenshot()
