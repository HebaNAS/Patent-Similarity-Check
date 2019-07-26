# Loading dependencies
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import glob
import os


def main():
    """
    This script segments a scan of a pdf page and extract what
    is likely to be figures or images in the document
    """


# Loop through all image folders
for folder in glob.glob('./temp/images/*'):

    i = 0

    # Loop through all images in the folder
    for image in glob.glob(folder + '/*'):
        print('Processing images in', image[14:27])

        # Read the image and get the dimensions
        img = cv.imread(image)
        h, w, _ = img.shape

        # Run tesseract method to get bounding boxes around recognized characters
        boxes = pytesseract.image_to_boxes(Image.open(image))

        i = 0

        # Loop through all bounding boxes
        for b in boxes.splitlines():
            b = b.split(' ')

            # Extract figures from a page and save them
            images = []

            # Check for dimensions of bound box, if they exceed 1000px for width and height
            # consider the box containing a figure and crop it out
            if (int(b[3]) - int(b[1]) > 1000) and ((h - int(b[2])) - (h - int(b[4])) > 1000):
                images.append([int(b[2]), int(b[4]), int(b[1]), int(b[3])])
                crop = img[images[0][0]:images[0]
                           [1], images[0][2]:images[0][3]]

                # Check if folder with the current document name exists
                if not os.path.exists('./temp/figures/' + image[14:27]):

                    # If folder does not exist, create it
                    os.makedirs('./temp/figures/' + image[14:27])

                print('Saving figures in document', image[14:27])
                plt.imsave('./temp/figures/' +
                           image[14:-4] + '_' + str(i) + '.png', crop)

                i += 1

if __name__ == '__main__':
    main()
