from abc import ABC, abstractmethod
import pymagnitude as magnitude
# from gensim.models import FastText
# from gensim.models import KeyedVectors
from numpy import zeros
import numpy as np
class Embeddings(ABC):
    """
    Abstract Base Class for Word Embeddings.
    This class should implement the polymorph function embeddings() to producs Embeddings from a list of tokens
    """

    padding_marker = '*none'

    def __init__(self, dimensions):
        """
        :param int dimensions: Dimensions of the Word Embedding Vectors
        :return: Embeddings Object
        """

        self.dimensions = dimensions
        super().__init__()

    @abstractmethod
    def embeddings(self, tokens):
        """
        This method will take a list of tokens and returns a list of Word Embeddings with the same size.

        :param list tokens: List of tokens to transform into Embeddings
        """

        raise NotImplementedError

class Magnitudes(Embeddings):
    """
    Handles the Embeddings using pymagnitude
    https://github.com/plasticityai/magnitude
    """

    def __init__(self, filepath='model\data\wiki-news-300d-1M.magnitude', dimensions=300):
        """
        Load the pretrained Embeddings

        :param string filename: Path to pymagnitude file as *.magnitude
        :param int dimensions: Dimensions of the Vectors (to generate zeros for padding)
        """

        self.dimensions = dimensions
        self.filepath = filepath
        self.vectors = magnitude.Magnitude(filepath)

    def embeddings(self, tokens):
        """
        Transforms a list of tokens into a list of embeddings

        :param list tokens: List of tokens to transform into Embeddings
        :return: List of embeddings for given tokens
        """
        return_list = []
        for token in tokens:
            if token == Embeddings.padding_marker:
                return_list.append(zeros(self.dimensions))
            elif token in self.vectors:
                vec = self.vectors.query(token)
                return_list.append(vec)
            else:
                # pymagnitude finds the most similar
                vec = self.vectors.query(token)
                return_list.append(vec)

        return return_list

# t = FastText.load_fasttext_format('model\data\cc.es.300.bin')
# token = input("pon la palabra:")

# if token in t:
#     print(t[token])

