import glob
import os
from PIL import Image
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

        # Check if folder with the current document name exists
        if not os.path.exists('./temp/images/' + doc[7:-4]):

            # If folder does not exist, create it
            os.makedirs('./temp/images/' + doc[7:-4])

        # Use convert_from_path function from pdf2image library to
        # make the conversion
        print('Converting document', doc[7:-4], '...')
        images = convert_from_path(
            doc, single_file=True, dpi=600, fmt='tiff', thread_count=6, output_folder='./temp/images/' + doc[7:-4])


if __name__ == '__main__':
    main()
