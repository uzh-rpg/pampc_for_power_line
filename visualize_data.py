import os
import random

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw


def plot_bounding_box(image, annotation_list):
    annotations = np.array(annotation_list)
    w, h = image.size
    mapping = ["negative", "postive"]
    plotted_image = ImageDraw.Draw(image)

    transformed_annotations = np.copy(annotations)
    transformed_annotations[:, [1, 3]] = annotations[:, [1, 3]] * w
    transformed_annotations[:, [2, 4]] = annotations[:, [2, 4]] * h

    transformed_annotations[:, 1] = transformed_annotations[:, 1] - (
        transformed_annotations[:, 3] / 2
    )
    transformed_annotations[:, 2] = transformed_annotations[:, 2] - (
        transformed_annotations[:, 4] / 2
    )
    transformed_annotations[:, 3] = (
        transformed_annotations[:, 1] + transformed_annotations[:, 3]
    )
    transformed_annotations[:, 4] = (
        transformed_annotations[:, 2] + transformed_annotations[:, 4]
    )

    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        plotted_image.rectangle(((x0, y0), (x1, y1)))

        plotted_image.text((x0, y0 - 10), mapping[int(obj_cls)])

    plt.imshow(np.array(image))
    plt.show()


def main():
    # Get any random annotation file
    annotation_path = "YOUR_PATH_TO_LABELS" 
    with open(annotation_path, "r") as file:
        annotation_list = file.read().split("\n")[:-1]
        annotation_list = [x.split(" ") for x in annotation_list]
        annotation_list = [[float(y) for y in x] for x in annotation_list]

    # Get the corresponding image file
    image_file = annotation_path.replace("labels", "images").replace(
        "txt", "png"
    )
    assert os.path.exists(image_file)

    # Load the image
    image = Image.open(image_file)

    # Plot the Bounding Box
    plot_bounding_box(image, annotation_list)


if __name__ == "__main__":
    main()

