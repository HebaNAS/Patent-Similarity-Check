import glob
import os
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def main():
    """
    This script converts all images in a given directory
    into text files
    """

    # Loop through all patent folders
    for folder in glob.glob('temp/images/US*'):
        patent_text = []

        # Loop through all pages images for each patent
        for image in glob.glob(folder + '/*.jpg'):
            # Use tesseract to extract text from each image
            patent_text.insert(0,pytesseract.image_to_string(Image.open(image)))

        # Write the extracted text into a file to use later
        with open('temp/text/' + image[25:39] + '.txt', 'w') as txt_file:
            for line in patent_text:
                txt_file.write(''.join(line) + '\n')

if __name__ == '__main__':
	main()