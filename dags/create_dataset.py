import xml.etree.ElementTree as ET
import xmltodict
import pandas as pd
import glob

def main():
    """
    This script reads an xml file into a tree structure and then traverse it
    in order to save it into a csv format as tabular data to be read into
    a dataframe using pandas
    """

    # Define the pandas dataframe with features needed
    cols = ['id', 'invention_title', 'abstract', 'claims', 'description', 'drawings_description', 'drawings_file_paths']
    patents_df = pd.DataFrame(columns=cols)
    
    # Loop through all folders and grab xml files
    for folder in glob.glob('./Dataset/*'):

        # Select only main xml file (folder[11:35]) and ignore supplementary ones
        # that have different name pattern
        for _file in glob.glob(folder + '/' + folder[10:34] + '.XML'):
            
            print('Processing document', folder[11:35])

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

                # Write extracted content to dataframe
                patents_df = patents_df.append(pd.Series([_id, invention_title, abstract_text, claims_text, \
                                                          description_text, drawings_description_text, \
                                                        drawings_file_paths], index=cols), ignore_index=True)
    
    # Write dataframe to csv file    
    patents_df.to_csv('./Dataset/patents_training.csv')

if __name__ == '__main__':
    main()
