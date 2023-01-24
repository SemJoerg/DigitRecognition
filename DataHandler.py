import os
import numpy as np
import pandas as pd
from PySide6.QtGui import QImage
import matplotlib.pyplot as plt

class DataHandler:

    def __init__(self, file_path: str, image_size: int):
        self.file_path = file_path
        self.image_size = image_size
        self.image_data = None
        self.label_data = None

        if os.path.exists(self.file_path):
            data = np.load(self.file_path)
            self.image_data = data["arr_0"]
            self.label_data = data["arr_1"]
            print(f"Data ({self.image_data.shape}):\n{self.image_data}\nLabels:\n{self.label_data}")

    def add_data_to_file(self, image: QImage, label: int) -> None:
        pixels = np.empty((self.image_size, self.image_size), np.int8)
        for row in range(image.height()):
            for colum in range(image.width()):
                pixel = 1 if image.pixel(colum, row) == 4294967295 else 0
                pixels[row, colum] = pixel

        if self.image_data is None:
            self.image_data = np.array([pixels], dtype=np.int8)
        else:
            self.image_data = np.append(self.image_data, [pixels], axis=0)
        if self.label_data is None:
            self.label_data = np.array([label], dtype=np.int8)
        else:
            self.label_data = np.append(self.label_data, [label], axis=None)

        np.savez(self.file_path, self.image_data, self.label_data)
        print(f"Data ({self.image_data.shape}):\n{self.image_data}\nLabels:\n{self.label_data}")

    def plot_data(self) -> None:
        plt.figure(figsize=(10, 10))
        for i in range(len(self.label_data)):
            if 10 ** 2 <= i+1:
                break

            plt.subplot(15, 15, i + 1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.imshow(self.image_data[i], cmap=plt.cm.binary)
            plt.xlabel(self.label_data[i])
        plt.tight_layout()
        plt.show()