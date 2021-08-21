
import numpy as np
import matplotlib.pyplot as plt

from skimage import io, color, filters
from skimage.transform import resize, rotate
from skimage.color import rgb2gray


def process_image(filepath='image_1318.jpg', shape=None, threshold=0.5):
    image = io.imread(filepath)
    grayscale = rgb2gray(image)

    if shape:
        grayscale = resize(grayscale, shape)
    
    return (grayscale <= threshold).astype(int)