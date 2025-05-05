<p align="center">
  <h2 align="center"> Autonomous Power Line Inspection with Drones via Perception-Aware MPC </h2>
  <p align="center">
    <a href="https://jiaxux.ing/">Jiaxu Xing*</a>
    ,
    <a href="https://giovanni-cioffi.netlify.app/">Giovanni Cioffi*</a>
    ,
    <a href="https://jhidalgocarrio.github.io/">Javier Hidalgo-Carrio</a>
    ,
    <a href="https://rpg.ifi.uzh.ch/people_scaramuzza.html">Davide Scaramuzza</a>
  </p>
  <p align="center"> <strong> IROS 2023</strong></p>
  <p align="center">
    Robotics and Perception Group, University of Zurich
  </p>
  <h3 align="center">

[![arXiv](https://img.shields.io/badge/arXiv-blue?logo=arxiv&color=%23B31B1B)](https://arxiv.org/abs/2304.00959)
[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-blue)](https://opensource.org/license/gpl-3-0)
[![YouTube](https://img.shields.io/badge/YouTube-red?logo=youtube)](https://www.youtube.com/watch?v=JA6h-Nv29pU)

 <div align="center"></div>
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=JA6h-Nv29pU">
    <img src="https://github-production-user-asset-6210df.s3.amazonaws.com/49942794/272397448-307dbdd7-c3e9-4613-a4ef-f6dc563812d6.png" alt="Power Line Inspection" width="600"/>
  </a>
</p>

# Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
  - [Dataset Structure](#-dataset-structure)
  - [Label Format](#label-format)
- [Line Detection](#line-detection)
  - [Inference Guide](#inference-guide)
  - [Inference Settings](#inference-settings)
- [Citation](#citation)

# Overview

This repository contains the implementation of our IROS 2023 paper on autonomous power line inspection using drones. The project consists of two main components:

1. **Perception Module** (This Repository)
   - Power line detector
   - Dataset structure and tools
   - Training and evaluation scripts

2. **Control Module** ([Agilicious Framework](https://github.com/uzh-rpg/agilicious))
   - Perception-aware Model Predictive Controller (MPC)
   - Access must be requested through the [Agilicious documentation](https://agilicious.readthedocs.io/en/latest/index.html)

# Dataset

In this work, we provide a hybrid dataset for power line inspection, which includes both synthetic and real-world data (overlayed with some synthetic line structure). The dataset is designed to train and evaluate the perception module of our system.

The dataset can be downloaded from the following [link](https://download.ifi.uzh.ch/rpg/powerline_tracking_dataset/power_line_dataset.zip). The dataset is organized into several folders, each containing images, labels, and masks. The images are divided into training, validation, and test sets.

## 📁 Dataset Structure

After downloading the dataset, you'll find the following organization:

```bash
📦 power_line_dataset
├── 📂 powerline_0_simple
│   ├── 📂 images
│   │   ├── 📂 train
│   │   │   ├── 🖼️ frame_0.png
│   │   │   ├── 🖼️ frame_1.png
│   │   │   └── ...
│   │   ├── 📂 test
│   │   │   ├── 🖼️ frame_0.png
│   │   │   ├── 🖼️ frame_1.png
│   │   │   └── ...
│   │   └── 📂 val
│   │       ├── 🖼️ frame_0.png
│   │       ├── 🖼️ frame_1.png
│   │       └── ...
│   │
│   ├── 📂 labels
│   │   ├── 📂 train
│   │   │   ├── 📄 frame_0.txt
│   │   │   ├── 📄 frame_1.txt
│   │   │   └── ...
│   │   ├── 📂 test
│   │   │   ├── 📄 frame_0.txt
│   │   │   ├── 📄 frame_1.txt
│   │   │   └── ...
│   │   └── 📂 val
│   │       ├── 📄 frame_0.txt
│   │       ├── 📄 frame_1.txt
│   │       └── ...
│   │
│   └── 📂 masks
│       ├── 📂 binary_masks
│       └── 📂 color_masks
├── 📂 power_line_1_forest
├── 📂 power_line_2_industrial
└── 📂 powerline_17_random_background
```

The dataset is organized into several folders from different environmental backgrounds, each containing images, labels, and masks. The images are divided into training, validation, and test sets. 

## Label Format

Each label file contains object annotations in YOLO format with one object per line. Each line consists of five space-separated values:

```
<class_id> <x_center> <y_center> <width> <height>
```

| Parameter | Description | Range |
|-----------|-------------|-------|
| class_id | Object class identifier (0 for power line) | Integer |
| x_center | Normalized center X coordinate | 0.0 - 1.0 |
| y_center | Normalized center Y coordinate | 0.0 - 1.0 |
| width | Normalized width of bounding box | 0.0 - 1.0 |
| height | Normalized height of bounding box | 0.0 - 1.0 |

Example:
```
0 0.775694 0.412500 0.445833 0.679167
```
This represents a power line where:
- Center is at 77.57% of image width and 41.25% of image height
- Bounding box is 44.58% of image width and 67.92% of image height

# Line Detection
## Inference Guide

First of all, you need to clone the submodule of the `yolov5` repository, which is used for the power line detection. You can do this by running the following command in your terminal:

```bash
git clone --recurse-submodules
``````

To perform inferences on custom images or videos using a pretrained network, first enter the yolo folder

```
cd yolov5
```

Then you will need to install the dependecies by

```
pip install -r requirements.txt
```
The inference will be done by using the script `detect.py`, here is the usage

```
python detect.py --weights path-to-your-weights --img 320 --source path-to-the-folder-contains-test-images
```

For example, if you place your model at `../pretrained_model/model_new.pt` (there is already one provided), and some of your test images or/and videos at `../test_images/`, then you could already start the inference by

```
python detect.py --weights ../pretrained_model/model_new.pt --img 320 --source ../test_images/
```

Then the inference results (images and/or videos with bounding boxes, class labels, and confidence) will be saved in newly generated folder in `./runs/expXX/`. You dont need to convert the video into the images, the pipeline will automatically detect it and at the end output the result in the same input format.

**REMARK:** There is no need to convert videos into images, this script could both handle images or videos)

If we need to apply for a filtering to our prediction based on the inference confidence (range 0 - 1), simply add the minimum filter value `C` using `--conf-thres C`, then the bounding boxes with lower confidence scores than `C` will not be displayed.

```
python detect.py --weights ../pretrained_model/model_new.pt --img 320 --source ../test_images/ --conf-thres C
```

## Quick Inference Guide
Parameters setting during inference, 

|  `Arguments` | Functionality  |
|---|---|
|  `--max_det` | Specify maximum detection number within an image  |
|  `--view-image` |   Interactive visualization of the detection result|
|  `--hide-labels` | Hide the detection labels in the visualization |
|  `--hide-conf` | Hide the the confidential score in the visualization |


# Citation

If you find this work useful, please consider citing:

```bibtex
@inproceedings{xing2023autonomous,
  title={Autonomous power line inspection with drones via perception-aware mpc},
  author={Xing, Jiaxu and Cioffi, Giovanni and Hidalgo-Carri{\'o}, Javier and Scaramuzza, Davide},
  booktitle={2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  pages={1086--1093},
  year={2023},
  organization={IEEE}
}

```
