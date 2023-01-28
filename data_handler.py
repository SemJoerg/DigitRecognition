from __future__ import annotations
import os
import numpy as np
import plotly.express as px
from PySide6.QtGui import QImage


class DataHandler:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.image_data: np.ndarray = None
        self.label_data: np.ndarray = None

        if os.path.exists(self.file_path):
            data = np.load(self.file_path)
            self.image_data: np.ndarray = data["arr_0"]
            self.label_data: np.ndarray = data["arr_1"]
            #print(f"Data ({self.image_data.shape}):\n{self.image_data}\nLabels:\n{self.label_data}")

    @staticmethod
    def image_to_nparray(image: QImage) -> np.ndarray:
        pixels = np.empty((image.height(), image.width()), np.int8)
        for row in range(image.height()):
            for colum in range(image.width()):
                pixel = 1 if image.pixel(colum, row) == 4294967295 else 0
                pixels[row, colum] = pixel
        return pixels

    def save_data(self):
        np.savez(self.file_path, self.image_data, self.label_data)
        print(f"Data ({self.image_data.shape}):\n{self.image_data}\nLabels:\n{self.label_data}")

    def add_data_to_file(self, image: QImage, label: int) -> None:
        pixels = DataHandler.image_to_nparray(image)

        if self.image_data is None:
            self.image_data = np.array([pixels], dtype=np.int8)
        else:
            self.image_data = np.append(self.image_data, [pixels], axis=0)
        if self.label_data is None:
            self.label_data = np.array([label], dtype=np.int8)
        else:
            self.label_data = np.append(self.label_data, [label], axis=None)

        self.save_data()

    def plot_data(self) -> None:
        data_length = len(self.label_data)
        if data_length <= 150:
            fig = px.imshow(self.image_data, title=self.file_path, binary_string=True, facet_col=0, facet_col_wrap=20)
        else:
            fig = px.imshow(self.image_data[data_length-100:data_length], title=self.file_path, binary_string=True, facet_col=0, facet_col_wrap=20)

        fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
        for annotation in fig.layout.annotations:
            index = int(annotation['text'][10:])
            if data_length <= 150:
                annotation['text'] = f'[{index}]  {self.label_data[index]}'
            else:
                annotation['text'] = f'[{index}]  {self.label_data[data_length-100:data_length][index]}'
        fig.show()

    def remove_index(self, *index: int) -> None:
        self.image_data = np.delete(self.image_data, index, axis=0)
        self.label_data = np.delete(self.label_data, index, axis=0)

    def add(self, data: DataHandler) -> None:
        if self.image_data is None:
            self.image_data = np.array(data.image_data, dtype=np.int8)
        else:
            self.image_data = np.append(self.image_data, data.image_data, axis=0)
        if self.label_data is None:
            self.label_data = np.array(data.label_data, dtype=np.int8)
        else:
            self.label_data = np.append(self.label_data, data.label_data, axis=None)
