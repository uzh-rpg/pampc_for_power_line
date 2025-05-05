import json
import os
import re

import cv2
import matplotlib.pyplot as plt
import torchvision
from torch.utils import data


def show_combined_imgae(image, label):
    x_center = label["x_center"]
    y_center = label["y_center"]
    width = label["width"]
    height = label["height"]
    is_counter_diagonal = label["is_counter_diagonal"]
    if is_counter_diagonal:
        class_label = "negative_line"
    else:
        class_label = "postive_line"
    cv2.rectangle(
        image,
        (
            int((x_center - 0.5 * width) * 720),
            int((y_center - 0.5 * height) * 480),
        ),
        (
            int((x_center + 0.5 * width) * 720),
            int((y_center + 0.5 * height) * 480),
        ),
        (0, 255, 0),
        2,
    )
    cv2.putText(
        image,
        class_label,
        (
            int((x_center + 0.5 * width) * 720) + 10,
            int((y_center + 0.5 * height) * 480),
        ),
        0,
        0.3,
        (0, 255, 0),
    )

    return image


class ImageDataset(data.Dataset):
    def __init__(self, img_path, label_path):
        self.data_path = img_path
        self.mask_dir_files = os.listdir(self.data_path)
        self.mask_dir_files.sort(key=lambda f: int(re.sub("\D", "", f)))
        self.len = len(os.listdir(self.data_path))
        self.transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.Resize((224, 224)),
                torchvision.transforms.ToTensor(),
                # torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]
        )

        with open(label_path) as f:
            self.json_label = json.load(f)

    def __len__(self):
        return self.len

    def __getitem__(self, index):
        frame_name = self.mask_dir_files[index]
        file_path = os.path.join(self.data_path, frame_name)
        # image_ = Image.open(file_path).convert('RGB')
        # if self.transform:
        #     image_ = self.transform(image_)
        image_ = cv2.imread(file_path)
        label_ = self.json_label[frame_name]

        return image_, label_


image_path = "YOUR_PATH_TO_IMAGES"
label_path = "YOUR_PATH_TO_LABELS"

dataset = ImageDataset(image_path, label_path)
for i in range(10):
    image, label = dataset[i]
    image = show_combined_imgae(image, label)
    plt.imshow(image)
    plt.show()
