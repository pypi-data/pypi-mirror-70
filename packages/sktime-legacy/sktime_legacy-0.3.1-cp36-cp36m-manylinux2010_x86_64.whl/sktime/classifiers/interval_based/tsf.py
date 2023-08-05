""" Time Series Forest Classifier (TSF).
Implementation of Deng's Time Series Forest, with minor changes
"""

__author__ = "Tony Bagnall"
__all__ = ["TimeSeriesForest"]

import numpy as np
import pandas as pd
import math
from sklearn.ensemble.forest import ForestClassifier
from sklearn.tree import DecisionTreeClassifier
from numpy import random
from copy import deepcopy
from sklearn.utils.multiclass import class_distribution
from sktime.utils.load_data import load_from_tsfile_to_dataframe as ld


class TimeSeriesForest(ForestClassifier):

    """ Time-Series Forest Classifier.

    TimeSeriesForest: Implementation of Deng's Time Series Forest, with minor changes
    @article
    {deng13forest,
     author = {H.Deng and G.Runger and E.Tuv and M.Vladimir},
              title = {A time series forest for classification and feature extraction},
    journal = {Information Sciences},
    volume = {239},
    year = {2013}
    
    Overview: Input n series length m
    for each tree
        sample sqrt(m) intervals
        find mean, sd and slope for each interval, concatenate to form new data set
        build decision tree on new data set
    ensemble the trees with averaged probability estimates
    
    This implementation deviates from the original in minor ways. It samples intervals with replacement and 
    does not use the splitting criteria tiny refinement described in deng13forest. This is an intentionally 
    stripped down, non configurable version for use as a hive-cote component. For a configurable tree based 
    ensemble, see sktime.classifiers.ensemble.TimeSeriesForestClassifier

    TO DO: handle missing values, unequal length series and multivariate problems
    
    Parameters
    ----------
    n_trees         : int, ensemble size, optional (default = 200)
    random_state    : int, seed for random, optional (default to no seed, I think!)
    min_interval    : int, minimum width of an interval, optional (default to 3)

    Attributes
    ----------
    n_classes    : int, extracted from the data
    num_atts       : int, extracted from the data
    n_intervals  : int, sqrt(num_atts)
    classifiers    : array of shape = [n_trees] of DecisionTree classifiers
    intervals      : array of shape = [n_trees][n_intervals][2] stores indexes of all start and end points for all classifiers
    dim_to_use     : int, the column of the panda passed to use (can be passed a multidimensional problem, but will only use one)
    
    """

    def __init__(self,
                 random_state = None,
                 min_interval=3,
                 n_trees = 200
                 ):
        super(TimeSeriesForest, self).__init__(
            base_estimator=DecisionTreeClassifier(criterion="entropy"),
            n_estimators=n_trees)

        self.random_state = random_state
        random.seed(random_state)
        self.n_trees=n_trees
        self.min_interval=min_interval
# The following set in method fit
        self.n_classes = 0
        self.series_length = 0
        self.n_intervals = 0
        self.classifiers = []
        self.intervals=[]
        self.classes_ = []

    def fit(self, X, y):
        """Build a forest of trees from the training set (X, y) using random intervals and summary features
        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_instances,series_length] or shape = [n_instances,n_columns]
            The training input samples.  If a Pandas data frame is passed it must have a single column (i.e. univariate
            classification. RISE has no bespoke method for multivariate classification as yet.
        y : array-like, shape =  [n_instances]    The class labels.

        Returns
        -------
        self : object
         """
        if isinstance(X, pd.DataFrame):
            if X.shape[1] > 1:
                raise TypeError("TSF cannot handle multivariate problems yet")
            elif isinstance(X.iloc[0,0], pd.Series):
                X = np.asarray([a.values for a in X.iloc[:,0]])
            else:
                raise TypeError("Input should either be a 2d numpy array, or a pandas dataframe with a single column of Series objects (TSF cannot yet handle multivariate problems")
        n_samps, self.series_length = X.shape

        self.n_classes = np.unique(y).shape[0]

        self.classes_ = class_distribution(np.asarray(y).reshape(-1, 1))[0][0]
        self.n_intervals = int(math.sqrt(self.series_length))
        if self.n_intervals==0:
            self.n_intervals = 1
        if self.series_length <self.min_interval:
            self.min_interval=self.series_length
        self.intervals=np.zeros((self.n_trees, 3 * self.n_intervals, 2), dtype=int)
        for i in range(0, self.n_trees):
            transformed_x = np.empty(shape=(3 * self.n_intervals, n_samps))
            # Find the random intervals for classifier i and concatentate features
            for j in range(0, self.n_intervals):
                self.intervals[i][j][0]=random.randint(self.series_length - self.min_interval)
                length=random.randint(self.series_length - self.intervals[i][j][0] - 1)
                if length < self.min_interval:
                    length = self.min_interval
                self.intervals[i][j][1] = self.intervals[i][j][0] + length
                # Transforms here, just hard coding it, so not configurable
                means = np.mean(X[:, self.intervals[i][j][0]:self.intervals[i][j][1]], axis=1)
                std_dev = np.std(X[:, self.intervals[i][j][0]:self.intervals[i][j][1]], axis=1)
                slope = self.lsq_fit(X[:, self.intervals[i][j][0]:self.intervals[i][j][1]])
                transformed_x[3*j]=means
                transformed_x[3*j+1]=std_dev
                transformed_x[3*j+2]=slope
            tree = deepcopy(self.base_estimator)
            transformed_x=transformed_x.T
            tree.fit(transformed_x, y)
            self.classifiers.append(tree)
        return self


    def predict(self, X):
        """
        Find predictions for all cases in X. Built on top of predict_proba
        Parameters
        ----------
        X : The training input samples. array-like or pandas data frame.
        If a Pandas data frame is passed, a check is performed that it only has one column.
        If not, an exception is thrown, since this classifier does not yet have
        multivariate capability.

        Returns
        -------
        output : array of shape = [n_test_instances]
        """

        proba=self.predict_proba(X)
        return [self.classes_[np.argmax(prob)] for prob in proba]

    def predict_proba(self, X):
        """
        Find probability estimates for each class for all cases in X.
        Parameters
        ----------
        X : The training input samples. array-like or sparse matrix of shape = [n_test_instances, series_length]
            If a Pandas data frame is passed (sktime format) a check is performed that it only has one column.
            If not, an exception is thrown, since this classifier does not yet have
            multivariate capability.

        Local variables
        ----------
        n_test_instances     : int, number of cases to classify
        series_length    : int, number of attributes in X, must match _num_atts determined in fit

        Returns
        -------
        output : array of shape = [n_test_instances, num_classes] of probabilities
        """
        if isinstance(X, pd.DataFrame):
            if X.shape[1] > 1:
                raise TypeError("TSF cannot handle multivariate problems yet")
            elif isinstance(X.iloc[0,0], pd.Series):
                X = np.asarray([a.values for a in X.iloc[:,0]])
            else:
                raise TypeError("Input should either be a 2d numpy array, or a pandas dataframe with a single column of Series objects (TSF cannot yet handle multivariate problems")

        n_test_instances, series_length = X.shape
        if series_length != self.series_length:
            raise TypeError(" ERROR number of attributes in the train does not match that in the test data")
        sums = np.zeros((X.shape[0],self.n_classes), dtype=np.float64)
        for i in range(0, self.n_trees):
            transformed_x = np.empty(shape=(3 * self.n_intervals, n_test_instances), dtype=np.float32)
            for j in range(0, self.n_intervals):
                means = np.mean(X[:, self.intervals[i][j][0]:self.intervals[i][j][1]], axis=1)
                std_dev = np.std(X[:, self.intervals[i][j][0]:self.intervals[i][j][1]], axis=1)
                slope = self.lsq_fit(X[:, self.intervals[i][j][0]:self.intervals[i][j][1]])
                transformed_x[3*j]=means
                transformed_x[3*j+1]=std_dev
                transformed_x[3*j+2]=slope
            transformed_x=transformed_x.T
            sums += self.classifiers[i].predict_proba(transformed_x)

        output = sums / (np.ones(self.n_classes) * self.n_estimators)
        return output

    def lsq_fit(self, Y):
        """ Find the slope for each series (row) of Y
        Parameters
        ----------
        Y: array of shape = [n_samps, interval_size]

        Returns
        ----------
        slope: array of shape = [n_samps]

        """
        x = np.arange(Y.shape[1]) + 1
        slope = (np.mean(x * Y, axis=1) - np.mean(x) * np.mean(Y, axis=1)) / ((x * x).mean() - x.mean() ** 2)
        return slope



if __name__ == "__main__":
    dataset = "Gunpoint"
    train_x, train_y =  ld.load_from_tsfile_to_dataframe(file_path="C:/temp/sktime_temp_data/" + dataset + "/", file_name=dataset + "_TRAIN.ts")

    print(train_x.iloc[0:10])

    tsf = TimeSeriesForest()
    tsf.fit(train_x.iloc[0:10], train_y[0:10])
    preds = tsf.predict(train_x.iloc[10:20])
    print(preds)
