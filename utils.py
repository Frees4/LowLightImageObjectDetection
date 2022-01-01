import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


def adjust_gamma(image, gamma=1.0):
    inverted_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inverted_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    return cv2.LUT(image, table)


def adjust_gamma_images(path_to_folder, folder):
    list_of_files = os.listdir(path_to_folder + folder)
    for file in list_of_files:
        image = cv2.imread(path_to_folder + folder + file)
        cv2.imwrite(path_to_folder + folder + file, adjust_gamma(image, 2))


def histogram_equalization(image):
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, image)
    return image


def histogram_equalization_images(path_to_folder, folder):
    list_of_files = os.listdir(path_to_folder + folder)
    for file in list_of_files:
        image = cv2.imread(path_to_folder + folder + file)
        cv2.imwrite(path_to_folder + folder + file, histogram_equalization(image))


def save_image_histogram(image, path):
    plt.hist(image.ravel(), 256, [0, 256])
    plt.savefig(path)

