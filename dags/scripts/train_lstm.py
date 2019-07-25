import pandas as pd
import numpy as np
from gensim.models.doc2vec import Doc2Vec
import multiprocessing
from tensorflow import keras
from tensorflow.keras import layers
from ast import literal_eval

# Allow multi processors
cores = multiprocessing.cpu_count()


def main():
    """
    This script builds and trains a Long Short Term Memory (LSTM)
    Neural Network using the previously trained word embeddings
    the model is saved at the end of the process
    """

    # Load the trained word embeddings model
    document_embeddings = Doc2Vec.load('models/document_embeddings.doc2vec')
    patents_df = pd.read_csv('Dataset/patents.csv')

    # Start building the lstm using tensorflow keras module
    # print(1 - spatial.distance.cosine(np.asarray(document_embeddings.docvecs[29]).reshape(1, -1),
    #                                   np.asarray(document_embeddings.infer_vector(list(patents_df['tokenized_text'][29]), alpha=0.01, min_alpha=0.025, epochs=20, steps=80)).reshape(1, -1)))


if __name__ == '__main__':
    main()
