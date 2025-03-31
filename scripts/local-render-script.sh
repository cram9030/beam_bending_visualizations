#!/bin/bash
# render_video.sh - Local script to render beam bending visualization in high definition

# Ensure conda environment is activated
if [[ -z "${CONDA_DEFAULT_ENV}" || "${CONDA_DEFAULT_ENV}" != "beam-animations" ]]; then
    echo "Activating beam-animations conda environment..."
    
    # Check if conda is available in PATH
    if command -v conda >/dev/null 2>&1; then
        # Try to activate the environment
        if conda env list | grep -q beam-animations; then
            eval "$(conda shell.bash hook)"
            conda activate beam-animations
        else
            echo "Error: beam-animations environment not found. Please create it with:"
            echo "conda env create -f environment.yml"
            exit 1
        fi
    else
        echo "Error: conda command not found in PATH"
        exit 1
    fi
fi

# Create media directory if it doesn't exist
mkdir -p media/videos

echo "Rendering individual animations in 4K quality..."
python scripts/render-all-script.py -qk

if [ $? -ne 0 ]; then
    echo "Error: Failed to render individual animations"
    exit 1
fi

echo "Combining animations into final video..."
python scripts/combine-video-script.py --output teaching_demo_4k.mp4 --sequence video_sequence.txt --quality 4K60

if [ $? -ne 0 ]; then
    echo "Error: Failed to combine animations"
    exit 1
fi

echo "Video rendering complete! Output file: teaching_demo_4k.mp4"
echo "Full process completed successfully."
