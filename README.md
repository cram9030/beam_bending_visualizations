# Beam Bending Animations

This repository contains Manim animations for a 10-minute teaching demonstration on beam bending, designed for first-year engineering students at the University of Southampton (FEEG1002 module).

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
python3 scripts/render_all.py -qm
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

## License

This project is licensed under the MIT License - see the LICENSE file for details.