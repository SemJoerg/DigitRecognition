import os
import numpy as np
from data_handler import DataHandler

main_data = DataHandler("main_data_shuffeled.npz")

files = []
for file in os.listdir("./DigitData"):
    if file.endswith(".npz"):
        files.append(DataHandler(os.path.join("./DigitData", file)))


def clear() -> None:
    os.system("clear")


def int_input(description: str = "") -> int:
    while True:
        try:
            return int(input(f"\n{description}>"))
            break
        except:
            pass


def select_data(include_main_datta: bool = True) -> DataHandler:
    while True:
        print("[0] BACK")
        if include_main_datta:
            print("[-1] main_data")

        for i, file in enumerate(files):
            print(f"[{i + 1}] {file.file_path}")

        u_input = int_input()

        if u_input == 0:
            return None
        if u_input == -1 and include_main_datta:
            return main_data
        if u_input <= len(files):
            return files[u_input - 1]
        return None


while True:
    print("""
    [0] Exit
    [1] View data
    [2] Remove from data
    [3] Add sub_data to main_data
    [4] Save main_data""")
    u_input = int_input()

    if u_input == 0:
        exit()
    if u_input == 1:
        temp_data = select_data()
        if temp_data is None:
            continue
        print(temp_data.image_data.shape)
        temp_data.plot_data()
    if u_input == 2:
        temp_input = -2
        indexes = []
        while True:
            temp_input = int_input("[-2] BACK\n[-1] Stop Entering Indexes\nEnter index: ")
            if temp_input == -1:
                break
            if temp_input == -2:
                break
            indexes.append(temp_input)

        if temp_input == -2:
            continue

        select_data().remove_index(indexes)
    if u_input == 3:
        temp_data = select_data(False)
        if temp_data is None:
            continue
        main_data.add(temp_data)
    if u_input == 4:
        main_data.save_data()
