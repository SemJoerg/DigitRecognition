import os
import numpy as np
import pandas as pd
from PySide6.QtGui import QImage


class DataHandler:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = pd.DataFrame(columns=["image", "classification"])

        if os.path.exists(self.file_path):
            self.df = pd.read_csv(self.file_path)
            print(self.df)

    def add_data_to_file(self, image: QImage, classification: str) -> None:
        pixels = np.empty(image.width() * image.height(), np.int8)

        for row in range(image.height()):
            for colum in range(image.width()):
                pixel = image.pixel(colum, row)
                pixels[row * image.width() + colum] = pixel

        self.df.loc[len(self.df)] = [pixels, classification]
        print(self.df)
        self.df.to_csv(self.file_path, index=False)

