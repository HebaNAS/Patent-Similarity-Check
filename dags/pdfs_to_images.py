import glob
import os
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

def main():
    """
    This script converts all pdf files in a given directory
    into images
    """

    # Loop through all files that have pdf extension
    for doc in glob.glob('./PDFs/*.pdf'):

        # Use convert_from_path function from pdf2image library to
        # make the conversion
        images = convert_from_path(doc, dpi=200, thread_count=4)

        # Save ouput images into temporary folder
        for i, image in zip(range(len(images)), images):
            
            # Check if folder with the current document name exists  
            if not os.path.exists('./temp/images/' + doc[7:-4]):

                # If folder does not exist, create it
                os.makedirs('./temp/images/' + doc[7:-4])
            
            # Save images of the current document
            image.save('./temp/images/' + doc[7:-4] + '/' + doc[7:-4] + '_p' + str(i) + '.jpg', 'JPEG')

if __name__ == '__main__':
	main()
