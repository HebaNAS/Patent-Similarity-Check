import xml.etree.ElementTree as ET
import xmltodict
import pandas as pd
import glob
import re
import subprocess
import os

def extract_from_text(text, start_term, end_term, end_term_num=False):
    """
    This function accepts a piece of text and extracts what's
    between any two given strings after finding their positions
    """
    
    # Get positions for the two strings
    boundary_start = re.search(start_term, text, re.MULTILINE)
    boundary_end = ''
    if end_term_num == False:
        boundary_end = re.search(end_term, text, re.MULTILINE)
    else:
        boundary_end = end_term
                    
    if boundary_start and boundary_end and end_term_num == False:
        if boundary_start.end() > boundary_end.start() and boundary_end.start() > 0:
            return text[boundary_start.end():boundary_end.start()]
        elif boundary_end.start() > boundary_start.end() and boundary_start.end() > 0:
            return text[boundary_start.end():boundary_end.start()]
    elif boundary_start and boundary_end and end_term_num == True:
            return text[boundary_start.end():boundary_end]
    else:
        return ' '

def main():
    """
    This script reads an xml file into a tree structure and then traverse it
    in order to save it into a csv format as tabular data to be read into
    a dataframe using pandas
    """

    # Define the pandas dataframe with features needed
    cols = ['id', 'invention_title', 'abstract', 'claims', 'description', 'drawings_description', 'drawings_file_paths', 'invention_background', 'cross_reference', 'summary', 'detailed_description']
    patents_df = pd.DataFrame(columns=cols)
    i = 0
    # Loop through all folders and grab xml files
    for folder in glob.glob('./Dataset/*'):

        # Select only main xml file (folder[11:35]) and ignore supplementary ones
        # that have different name pattern
        for _file in glob.glob(folder + '/' + folder[10:34] + '.XML'):
            if i <= 4:
                print('Processing document', folder[10:34])

                # Parse xml tree
                tree = ET.parse(_file)
                root = tree.getroot()

                # Placeholder for text content
                abstract_text = ''
                claims_text = ''
                description_text = ''
                drawings_description_text = ''
                drawings_file_paths = []

                # Traverse XML tree and extract data we need
                if (root[0].tag == 'us-bibliographic-data-application'):

                    # Extract document number as id
                    _id = root[0].find('publication-reference').find('document-id').find('doc-number').text
                    
                    # Extract invention title
                    invention_title = root[0].find('invention-title').text
                    
                # Extract abstract
                abstract = root.find('abstract')
                
                # Extract claims
                claims = root.find('claims')
                
                # Extract all description
                description = root.find('description')
                
                # Extract drawings description (if present)
                if root.find('drawings') != None:
                    drawings_description = root.find('description').find('description-of-drawings')
                    
                # Extract drawings paths (if present)
                if root.find('drawings') != None:
                    drawings = root.find('drawings')

                # Store all paragraphs in the abstract section
                for child in abstract:
                    if (child.text != None):
                        abstract_text += child.text + '\n'

                # Store all paragraphs in the claims section
                for child in claims:
                    claims_text += ''.join(child.itertext()).replace('\n', ' ')
                    
                # Store all paragraphs in the description section
                for child in description:
                    description_text += ''.join(child.itertext()) + ' '
                    
                # Store all paragraphs in the drawings description section
                if drawings_description:
                    for child in drawings_description:
                        drawings_description_text += ''.join(child.itertext()) + ' '
                        
                # Store all drawings file paths
                if drawings:
                    for child in drawings:
                        drawings_file_paths.append(child[0].get('file'))

                ###############################
                ## Further text segmentation ##
                ###############################
                
                # Extract Background section
                invention_col = []
                for index, row in patents_df.iterrows():
                    invention_col.append(extract_from_text(row['description'], \
                    '([A-Z])*BACKGROUND(([A-Z])*(\s))*', \
                    '([A-Z])*SUMMARY(([A-Z])*(\s))*'))

                # Extract cross reference section
                ref_col = []
                for index, row in patents_df.iterrows():
                    invention_col.append(extract_from_text(row['description'], \
                    'CROSS-REFERENCE(([A-Z])*(\s))*', \
                    'in their entirety'))

                # Extract summary section
                summary_col = []
                for index, row in patents_df.iterrows():
                    summary_col.append(extract_from_text(row['description'], \
                    '([A-Z])*SUMMARY(([A-Z])*(\s))*', \
                    '([A-Z])*DESCRIPTION(([A-Z])*(\s))*'))

                # Extract detailed description section
                ddesc_col = []
                for index, row in patents_df.iterrows():
                    ddesc_col.append(extract_from_text(row['description'], \
                    '([A-Z])*DETAILED DESCRIPTION(([A-Z])*(\s))*', \
                    len(str(row['description'])), True))

                # Write extracted content to dataframe
                patents_df = patents_df.append(pd.Series([_id, invention_title, abstract_text, claims_text, \
                                                            description_text, drawings_description_text, \
                                                            drawings_file_paths, invention_col, \
                                                            ref_col, summary_col, \
                                                            ddesc_col], index=cols), ignore_index=True) 
        i += 1

    ###################################
    ## Extract chemical compounds as ##
    ##       SMILES notation         ##
    ##   from the provided images    ##
    ###################################
    m = 0
    # # Loop through all folders and grab .tif image files
    # for folder in glob.glob('./Dataset/*'):

    #     print('Recognizing structures in file', folder[10:])

    #     if m < 1:

    #         # Select only main tif file (folder[11:]) and ignore supplementary ones
    #         for _file in glob.glob(folder + '/*.TIF'):
                
    #             # Check if folder with the current document name exists
    #             if not os.path.exists('../temp/chemical-names-smiles/' + folder[10:]):

    #                 # If folder does not exist, create it
    #                 os.makedirs('../temp/chemical-names-smiles/' + folder[10:])
        
    #             # Run OSRA, the chemical structure OCR library (in shell)
    #             subprocess.check_call(['osra', _file, \
    #                                 '-w ../temp/chemical-names-smiles/' + str(_file[10:-4]) + '.txt'])
    #     m += 1

    # Loop through all folders and grab generated text files
    smiles_col = []

    for folder in glob.glob('./temp/chemical-names-smiles/*'):
    
        print('Reading SMILES in file', folder[29:])
        smiles_for_one = []
    
        # Select only main tiff file (folder[11:]) and ignore supplementary ones
        for _file in glob.glob(folder + '/*.txt'):

            # Read each file and append each line that represents a compound
            # to an array
            one = ''

            with open(_file, 'r') as smiles_file:
                one = smiles_file.readline()

            if one != '':
                smiles_for_one.append(one.replace('\n', ''))
    
    if len(smiles_for_one) != 0:
        smiles_col.append(smiles_for_one)    
    

    ###################################
    ## Extract chemical compounds as ##
    ##         InChI notation        ##
    ##      from the patent text     ##
    ###################################

    # Get full description section
    inchi = []

    for index, row in patents_df.iterrows():
        # Check if folder with the current document name exists
        if not os.path.exists('./temp/patent_text'):

            # If folder does not exist, create it
            os.makedirs('./temp/patent_text')
        
        # Write description in a text file
        with open('./temp/patent_text/US' + row['id'] + '.txt', 'w') as patent_text:
            patent_text.write(row['description'])

    # Loop through all files and grab text files

    for _file in glob.glob('./temp/patent_text/*.txt'):
        print(_file[19:])
        # Check if folder with the current document name exists
        if not os.path.exists('./temp/chemical-names-inchi/'):

            # If folder does not exist, create it
            os.makedirs('./temp/chemical-names-inchi/')
    
        print('Extracting chemical names from document', _file[19:])

        # Run ChemSpot, the Chemical named entity recognition library (in shell)
        subprocess.check_call(['java', '-Xmx2G', '-jar', './chemspot-2.0/chemspot.jar', \
            '-t', _file, '-o', './temp/chemical-names-inchi/' + _file[19:-4] + '.txt'])   
     
    
    # Loop through all files and grab text files
    for _file in glob.glob('./temp/chemical-names-inchi/*.txt'):
        
        inchi_results = []

        # Read each file 
        with open(_file, 'r') as f:
            inchi_results.append(str(f.readline()))

        inchi.append(inchi_results)

    print(inchi)
    
    # Write dataframe to csv file    
    patents_df.to_csv('./Dataset/patents_training.csv')

if __name__ == '__main__':
    main()
