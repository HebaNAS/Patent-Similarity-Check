import glob
import os
from PIL import Image
import cv2 as cv
import numpy as np


def main():
    """
    This script preprocess scanned images to enhance text recognition
    later on
    """

    # Loop through all folders that have converted images from pdfs
    for folder in glob.glob('./temp/images/*'):

        i = 0

        # Loop through all images in the folder
        for image in glob.glob(folder + '/*'):

            # Apply thresholding to increase constrast of black characters
            # and increase tesseract reading accuracy
            img = cv.imread(image, 0)
            ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

            # Crop header and footer of each page and
            # remove white borders on the sides
            crop_img = img[800:6300, 500:4600]

            # Change color space to be compatible with the format to save
            crop_img = cv.cvtColor(crop_img, cv.COLOR_BGR2RGB)

            # Save images of the current document
            print('Saving image', str(i), '...')
            cv.imwrite(image[:-3] + 'ppm', crop_img)
            os.remove(image)

            i += 1


if __name__ == '__main__':
    main()
