import pandas as pd
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import multiprocessing
from tqdm import tqdm
from ast import literal_eval
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial

# Allow multi processors
cores = multiprocessing.cpu_count()
epochs = 200


class TaggedPatentDocument(object):
    """
    This class tags documents to convert them into a suitable
    format for Doc2Vec
    """

    def __init__(self, docs):
        self.labels_list = docs.iloc[:, 0].to_list()
        self.doc_tokens_list = docs.iloc[:, 1].to_list()

    def __iter__(self):
        for idx, doc_tokens in enumerate(self.doc_tokens_list):
            yield TaggedDocument(doc_tokens, [self.labels_list[idx]])


def main():
    """
    This script trains a Doc2Vec model to create sentence embeddings
    for the given documents and store them
    """

    tagged_patents = []

    # Read tagged documents from csv file
    patents_df = pd.read_csv('Dataset/patents.csv')

    # Tag documents to convert them into a suitable format for Doc2Vec
    for p in TaggedPatentDocument(patents_df):
        tagged_patents.append(p)

    # Create model definition
    model = Doc2Vec(dm=0, hs=1, vector_size=300, min_count=3,
                    workers=cores, epochs=epochs)

    # Build vocabulary from documents
    model.build_vocab([x for x in tqdm(tagged_patents)])

    # Start training the model
    for epoch in range(epochs):
        print("Training epoch {}".format(epoch + 1))
        model.train([x for x in tqdm(tagged_patents)],
                    total_examples=len(tagged_patents), epochs=model.epochs)
        model.alpha = model.alpha - 0.002
        model.min_alpha = model.alpha

    model.save('models/document_embeddings.doc2vec')
    print('Model saved..')

    # Use the trained model to infer vector for sentences in the patent documents
    dim = 300

    document_vector = []

    for index, row in patents_df.iterrows():
        print('Getting document vector', index, '...')
        document = literal_eval(row[1])
        document_vector.append(model.docvecs[index])

    # Write results to a dataframe
    patents_tagged = pd.DataFrame(
        {'tagged_patents': tagged_patents})
    patents_vector = pd.DataFrame(
        {'document_vector': document_vector})

    # Write dataframe to csv file
    patents_df = pd.concat(
        [patents_df, patents_tagged, patents_vector], axis=1)

    print(1 - spatial.distance.cosine(np.asarray(model.docvecs[0]).reshape(1, -1),
                                      np.asarray(model.infer_vector(literal_eval(patents_df['tokenized_text'][0]), alpha=0.01, min_alpha=0.025, steps=20)).reshape(1, -1)))

    # patents_df.to_csv('Dataset/patents.csv', index=False)


if __name__ == '__main__':
    main()
