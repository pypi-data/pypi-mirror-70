import sys

import numpy as np
import pandas as pd
import scipy.stats

from sktime.transformers.dictionary_based.PAA import PAA
from sktime.utils.load_data import load_from_tsfile_to_dataframe as load_ts
from sktime.transformers.base import BaseTransformer
#    TO DO: verify this returned pandas is consistent with sktime definition. Timestamps?


class SAX(BaseTransformer):
    __author__ = "Matthew Middlehurst"
    """ SAX (Symbolic Aggregate approXimation) Transformer, as described in 
    Jessica Lin, Eamonn Keogh, Li Wei and Stefano Lonardi,
    "Experiencing SAX: a novel symbolic representation of time series"
    Data Mining and Knowledge Discovery, 15(2):107-144
    
    Overview: for each series: 
        run a sliding window across the series
        for each window
            shorten the series with PAA (Piecewise Approximate Aggregation)
            discretise the shortened seried into fixed bins
            form a word from these discrete values     
    by default SAX produces a single word per series (window_size=0). 
    SAX returns a pandas data frame where column 0 is the histogram (sparse pd.series)
    of each series.

    Parameters
    ----------
        word_length:         int, length of word to shorten window to (using PAA) (default 8)
        alphabet_size:       int, number of values to discretise each value to (default to 4)
        window_size:         int, size of window for sliding. If 0, uses the whole series (default to 0)
        remove_repeat_words: boolean, whether to use numerosity reduction (default False)
        save_words:          boolean, whether to use numerosity reduction (default False)

    Attributes
    ----------
        words:      histor = []
        breakpoints: = []
        num_insts = 0
        num_atts = 0
                    
            """
    def __init__(self,
                 word_length=8,
                 alphabet_size=4,
                 window_size=0,
                 remove_repeat_words=False,
                 save_words=False
                 ):
        self.word_length = word_length
        self.alphabet_size = alphabet_size
        self.window_size = window_size
        self.remove_repeat_words = remove_repeat_words
        self.save_words = save_words

        self.words = []
        self.breakpoints = []

        self.num_insts = 0
        self.num_atts = 0

    def transform(self, X):
        """

        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samples, num_atts]
            The training input samples.  If a Pandas data frame is passed, the column 0 is extracted

        Returns
        -------
        dims: Pandas data frame with first dimension in column zero
        """
        if self.alphabet_size < 2 or self.alphabet_size > 4:
            raise RuntimeError("Alphabet size must be an integer between 2 and 4")
        if self.word_length < 1 or self.word_length > 16:
            raise RuntimeError("Word length must be an integer between 1 and 16")
        if isinstance(X, pd.DataFrame):
            if X.shape[1] > 1:
                raise TypeError("SAX cannot handle multivariate problems yet")
            elif isinstance(X.iloc[0,0], pd.Series):
                X = np.asarray([a.values for a in X.iloc[:,0]])
            else:
                raise TypeError("Input should either be a 2d numpy array, or a pandas dataframe with a single column of Series objects (TSF cannot yet handle multivariate problems")

        self.num_atts = X.shape[1]

        if self.window_size == 0:
            self.window_size = self.num_atts

        self.breakpoints = self.generate_breakpoints()
        self.num_insts = X.shape[0]

        bags = pd.DataFrame()
        dim = []

        for i in range(self.num_insts):
            bag = {}
            lastWord = None

            words = []

            num_windows_per_inst = self.num_atts - self.window_size + 1
            split = np.array(X[i, np.arange(self.window_size)[None, :] + np.arange(num_windows_per_inst)[:, None]])

            split = scipy.stats.zscore(split, axis=1)

            paa = PAA(num_intervals=self.word_length)
            patterns = paa.fit_transform(split)
            patterns = np.asarray([a.values for a in patterns.iloc[:, 0]])

            for n in range(patterns.shape[0]):
                pattern = patterns[n, :]
                word = self.create_word(pattern)
                words.append(word)
                lastWord = self.add_to_bag(bag, word, lastWord)

            if self.save_words:
                self.words.append(words)

            dim.append(pd.Series(bag))

        bags[0] = dim

        return bags

    def create_word(self, pattern):
        word = BitWord()

        for i in range(self.word_length):
            for bp in range(self.alphabet_size):
                if pattern[i] <= self.breakpoints[bp]:
                    word.push(bp)
                    break

        return word

    def add_to_bag(self, bag, word, last_word):
        if self.remove_repeat_words and word.word == last_word:
            return last_word
        if word.word in bag:
            bag[word.word] += 1
        else:
            bag[word.word] = 1

        return word.word

    def generate_breakpoints(self):
        # Pre-made gaussian curve breakpoints from UEA TSC codebase
        return {
            2: [0, sys.float_info.max],
            3: [-0.43, 0.43, sys.float_info.max],
            4: [-0.67, 0, 0.67, sys.float_info.max],
            5: [-0.84, -0.25, 0.25, 0.84, sys.float_info.max],
            6: [-0.97, -0.43, 0, 0.43, 0.97, sys.float_info.max],
            7: [-1.07, -0.57, -0.18, 0.18, 0.57, 1.07, sys.float_info.max],
            8: [-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15, sys.float_info.max],
            9: [-1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22, sys.float_info.max],
            10: [-1.28, -0.84, -0.52, -0.25, 0.0, 0.25, 0.52, 0.84, 1.28, sys.float_info.max]
        }[self.alphabet_size]


class BitWord:
    # Used to represent a word for dictionary based classifiers such as BOSS an BOP.
    # Can currently only handle an alphabet size of <= 4 and word length of <= 16.
    # Current literature shows little reason to go beyond this, but the class will need changes/expansions
    # if this is needed.

    def __init__(self,
                 word=0,
                 length=0):
        self.word = word
        self.length = length
        self.bits_per_letter = 2  # this ^2 == max alphabet size
        self.word_space = 32  # max amount of bits to be stored, max word length == this/bits_per_letter

    def push(self, letter):
        # add letter to a word
        self.word = (self.word << self.bits_per_letter) | letter
        self.length += 1

    def shorten(self, amount):
        # shorten a word by set amount of letters
        self.word = self.right_shift(self.word, amount * self.bits_per_letter)
        self.length -= amount

    def word_list(self):
        # list of input integers to obtain current word
        word_list = []
        shift = self.word_space - (self.length * self.bits_per_letter)

        for i in range(self.length-1, -1, -1):
            word_list.append(self.right_shift(self.word << shift, self.word_space - self.bits_per_letter))
            shift += self.bits_per_letter

        return word_list

    @staticmethod
    def word_list(word, length):
        # list of input integers to obtain current word
        word_list = []
        shift = 32 - (length * 2)

        for i in range(length-1, -1, -1):
            word_list.append(BitWord.right_shift(word << shift, 32 - 2))
            shift += 2

        return word_list

    @staticmethod
    def right_shift(left, right):
        return (left % 0x100000000) >> right


if __name__ == "__main__":
    testPath="Z:\\ArchiveData\\Univariate_ts\\Chinatown\\Chinatown_TRAIN.ts"
    train_x, train_y =  load_ts(testPath)

    print("Correctness testing for SAX using Chinatown")
    print("First case used for testing")
    print(train_x.iloc[0,0])
    p = SAX(window_size=0, alphabet_size=4,word_length=8,save_words=False)
    print("Test 1: window_size =0, result should be single word for each series")
    x2 = p.transform(train_x)
    print("Correct single series SAX for case 1: = b,a,a,b,d,d,d,b")
    print("Transform mean case 1: =")
    word = BitWord.word_list(x2.iloc[0, 0].keys()[0], 8)
    print(word)

