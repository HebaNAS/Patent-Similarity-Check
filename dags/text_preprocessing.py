import pandas as pd
import re
import glob
import string
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def preprocessText(text):
    """
    This script parses text and removes stop words
    """

    # Convert all text into lowercase
    text = text.lower()

    # Remove new line character
    text = text.replace('\n', '')
    
    return text

def tokenize_text(text):
    """
    This script tokenizes text
    """

    # Split text into sentences
    sentences = sent_tokenize(text)

    return sentences

def main():
    """
    This script preprocesses text to remove stop words and other
    punctuation symbols
    """

    tokenized_patent = []
    file_ids = []
    patents_df = pd.DataFrame(columns=['file_id', 'tokenized_text'])

    # Loop through all patent files
    for f in glob.glob('temp/text/*.txt'):
        patent = ''
        file_ids.append(f[10:-4])

        # Read each patent text file
        with open(f, 'r') as txt_file:
            for line in txt_file:
                # Apply the preprocessing function to patent text
                patent += preprocessText(line)

        # Tokenize patent text
        tokenized_patent = tokenize_text(patent)

        # Write results to a dataframe
        patents_df = patents_df.append({'file_id': f[10:-4], 'tokenized_text': tokenized_patent}, ignore_index=True)

    # Write dataframe to csv file
    patents_df.to_csv('Dataset/patents.csv', index=False)                                 

if __name__ == '__main__':
	main()