import pandas as pd
import wget
import os
from PIL import Image

validation = pd.read_csv("data/Validation_GCC-1.1.0-Validation.tsv", sep="\t")

train = pd.read_csv("data/Train_GCC-training.tsv", sep="\t")

val_train = {"validation": validation, "train": train}


def download_files():
    val_train = {"validation": "https://storage.cloud.google.com/gcc-data/Validation/GCC-1.1.0-Validation.tsv?_ga=2.141047602.-1896153081.1529438250",
                 "train": "https://storage.cloud.google.com/gcc-data/Train/GCC-training.tsv?_ga=2.191230122.-1896153081.1529438250"}
    for folder, url in val_train.keys():
        wget.download(url, "data/".format(folder))


def download_image_file(filename, file, starting_row=0):
    """
    Goes through the dataframe, tries to download photos based on the link and renames them based on their index
    :param filename: string
    :param file: pd.DataFrame
    :param starting_row: integer (where to start from if you've already done part of the job before)
    """
    rows = max(file.index)
    for row in filter(lambda x: x > starting_row, file.index):
        if row % 100 == 0:
            print("{:.2%}: {}/{}".format(row / rows, row, rows))
        if not os.path.exists("data/{}/img/{}.jpg".format(filename, row)):
            try:
                local_image_filename = wget.download(file.iloc[row][1], "data/{}/img/{}.jpg".format(filename, row))
            except EnvironmentError:
                continue


def download_image_files():
    for filename, file in val_train.items():
        download_image_file(filename, file)
    return 0


def check_img_folder(foldername,starting_file="1.jpg"):
    delete = 0
    folder = "data/{}/img/".format(foldername)
    for file in filter(lambda x: x > starting_file, filter(lambda x: x.endswith(".jpg"), os.listdir(folder))):
        try:
            img = Image.open(folder + file)
            img.verify()
            img.close
        except:
            os.remove(folder + file)
            delete += 1
    print("{} incomplete files were deleted".format(delete))


def check_img_folders():
    for foldername in val_train.keys():
        check_img_folder(foldername)


def extract_text(filename, file):
    for row in file.index:
        if os.path.exists("data/{}/img/{}.jpg".format(filename, row)):
            with open("data/{}/text/{}.txt".format(filename, row), "w", encoding="utf-8") as text_file:
                text_file.write(file.iloc[row][0])


def extract_texts():
    for filename, file in val_train.items():
        extract_text(filename, file)
    return 0