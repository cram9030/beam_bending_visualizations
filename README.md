# Beam Bending Animations

This repository contains Manim animations for a 10-minute teaching demonstration on beam bending, designed for first-year engineering students.

## Project Overview

This project creates visualizations that explain:
- Different types of beams (simply supported, cantilever, fixed)
- Basic beam bending principles
- Stress and strain distributions
- Moment diagrams
- Real-world applications

## Setup

### Prerequisites

- Python 3.8 or higher
- FFmpeg
- Cairo
- Latex
- xdg-utils

#### Prequisistes Install

```bash
sudo apt-get update
sudo apt-get install xdg-utils
sudo apt-get install texlive texlive-latex-extra texlive-fonts-recommended texlive-science texlive-xetex
```

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/beam-bending-animations.git
cd beam-bending-animations
```

2. Installiation

```bash
# Create and activate a conda environment
conda env create -f environment.yml
conda activate beam-animations
```

## Usage

### Render Individual Scenes

To render a specific scene:

```bash
manim -qm animations/scenes/intro-scene.py IntroScene
```

Quality options:
- `-ql`: Low quality (faster rendering)
- `-qm`: Medium quality
- `-qh`: High quality
- `-qk`: 4K quality

### Render All Animations

To render all animations:

```bash
python3 scripts/render-all-script.py -qm
```

### Create Final Video

To combine all rendered animations into the final teaching demonstration:

```bash
python3 scripts/combine-video-script.py --output teaching_demo.mp4 --sequence video_sequence.txt
```

## Project Structure

- `animations/`: Animation source files
  - `scenes/`: Individual animation scenes
  - `utils/`: Utility functions
- `assets/`: Static resources
- `scripts/`: Helper scripts
- `output/`: Generated animations (not tracked in git)

# GitHub Actions for Automatic Video Rendering

This repository includes a GitHub Action workflow that automatically renders the beam bending visualization in high definition (4K). The workflow can be triggered in two ways:

1. **Automatically**: Whenever code is pushed to the `main` branch
2. **Manually**: Through the GitHub Actions tab in the repository

## How It Works

The GitHub Action performs the following steps:

1. Sets up a Conda environment using the `environment.yml` file
2. Installs necessary system dependencies (ffmpeg, LaTeX, etc.)
3. Renders all individual animation scenes in 4K quality
4. Combines the rendered scenes into the final teaching demonstration video
5. Uploads the video as an artifact for download
6. Creates a GitHub release with the rendered video (only for pushes to main)

## Triggering the Workflow Manually

To trigger the workflow manually:

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Render Beam Bending Visualization" workflow
3. Click on the "Run workflow" button
4. Select the branch you want to run the workflow on
5. Click "Run workflow"

## Accessing the Rendered Video

After the workflow completes successfully, you can access the rendered video in two ways:

1. **Download as an artifact**:
   - Go to the completed workflow run
   - Scroll to the bottom to find the "Artifacts" section
   - Click on "beam-bending-video" to download

2. **From GitHub Releases** (for pushes to main):
   - Go to the "Releases" section of your repository
   - Find the latest release
   - Download the attached video file

## Customizing the Workflow

You can customize the workflow by editing the `.github/workflows/render-beam-bending.yml` file:

- Change the quality of the rendering by modifying the `-qk` parameter to `-ql` (low), `-qm` (medium), or `-qh` (high)
- Modify the output file name or location
- Add additional steps for further processing or deployment

## Troubleshooting

If the workflow fails, check the following:

1. Ensure all dependencies are correctly specified in the `environment.yml` file
2. Verify that the scripts are executable and have the correct paths
3. Check the workflow logs for specific error messages
4. Ensure your repository has sufficient GitHub Actions minutes available

For detailed logs and troubleshooting, click on the specific workflow run in the Actions tab.

## License

This project is licensed under the MIT License - see the LICENSE file for details.