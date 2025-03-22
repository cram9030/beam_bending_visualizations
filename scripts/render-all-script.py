#!/usr/bin/env python3
# scripts/render_all.py
"""
Script to render all animations in the project with specified quality.
Run this script from the project root directory.
"""

import os
import subprocess
import sys
import glob

# Quality options:
# -ql: Low quality, faster rendering
# -qm: Medium quality
# -qh: High quality
# -qk: 4K quality
QUALITY = "-qm"  # Default to medium quality

def main():
    print("Starting to render all animations...")
    
    # Get all scene files
    scene_files = glob.glob("animations/scenes/*.py")
    
    if not scene_files:
        print("No scene files found in 'animations/scenes/' directory.")
        return
    
    # Process command line arguments
    if len(sys.argv) > 1:
        global QUALITY
        if sys.argv[1] in ["-ql", "-qm", "-qh", "-qk"]:
            QUALITY = sys.argv[1]
    
    # Render each scene
    for scene_file in scene_files:
        render_scenes_in_file(scene_file)
    
    print("All animations rendered successfully!")

def render_scenes_in_file(scene_file):
    """Render all scenes in a given file."""
    # Extract filename without extension
    basename = os.path.basename(scene_file)
    module_name = os.path.splitext(basename)[0]
    
    print(f"Processing file: {basename}")
    
    # Import the module to get scene classes
    sys.path.insert(0, ".")
    module = __import__(f"animations.scenes.{module_name}", fromlist=["*"])
    
    # Find all scene classes in the module
    scene_classes = []
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type) and attr.__module__ == module.__name__ and attr_name.endswith("Scene"):
            scene_classes.append(attr_name)
    
    if not scene_classes:
        print(f"No scene classes found in {basename}")
        return
    
    # Render each scene
    for scene_class in scene_classes:
        render_scene(scene_file, scene_class)

def render_scene(scene_file, scene_class):
    """Render a specific scene from a file."""
    print(f"Rendering scene: {scene_class}")
    
    # Construct the command
    cmd = [
        "python", "-m", "manim", 
        scene_file, scene_class,
        QUALITY,
        "-o", f"{scene_class.lower()}"
    ]
    
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully rendered {scene_class}")
    except subprocess.CalledProcessError as e:
        print(f"Error rendering {scene_class}: {e}")

if __name__ == "__main__":
    main()
