""" KNN time series classification built on sklearn KNeighborsClassifier

"""

__author__ = "Jason Lines"
__all__ = ["KNeighborsTimeSeriesClassifier"]

from scipy import stats
from sklearn.utils.extmath import weighted_mode
from sklearn.neighbors.classification import KNeighborsClassifier
from functools import partial
from distutils.version import LooseVersion
import warnings
import numpy as np
from scipy.sparse import issparse
from sklearn.metrics import pairwise_distances_chunked
from sklearn.model_selection import GridSearchCV, LeaveOneOut
from sklearn.utils import gen_even_slices
from sklearn.utils.multiclass import check_classification_targets
from sklearn.utils.validation import check_is_fitted
from sklearn.utils import Parallel, delayed, effective_n_jobs
from sklearn.utils._joblib import __version__ as joblib_version
from sklearn.exceptions import DataConversionWarning
from sktime.distances.elastic_cython import dtw_distance, wdtw_distance, ddtw_distance, wddtw_distance, lcss_distance, erp_distance, msm_distance, twe_distance
from sktime.distances.mpdist import mpdist
from sklearn.utils.validation import check_array
from sklearn.neighbors.base import _check_weights, _get_weights
import pandas as pd

"""
Please note that many aspects of this class are taken from scikit-learn's KNeighborsTimeSeriesClassifier
class with necessary changes to enable use with time series classification data and distance measures.

TO-DO: add a utility method to set keyword args for distance measure parameters (e.g. handle the parameter
name(s) that are passed as metric_params automatically, depending on what distance measure is used in the
classifier (e.g. know that it is w for dtw, c for msm, etc.). Also allow long-format specification for
non-standard/user-defined measures
e.g. set_distance_params(measure_type=None, param_values_to_set=None, param_names=None)

"""


class KNeighborsTimeSeriesClassifier(KNeighborsClassifier):
    """
    An adapted version of the scikit-learn KNeighborsClassifier to work with time series data.

    Necessary changes required for time series data:
        -   calls to X.shape in kneighbors, predict and predict_proba.
            In the base class, these methods contain:
                n_samples, _ = X.shape
            This however assumes that data must be 2d (a set of multivariate time series is 3d). Therefore these methods
            needed to be overridden to change this call to the following to support 3d data:
                n_samples = X.shape[0]
        -   check array has been disabled. This method allows nd data via an argument in the method header. However, there
            seems to be no way to set this in the classifier and allow it to propagate down to the method. Therefore, this
            method has been temporarily disabled (and then re-enabled). It is unclear how to fix this issue without either
            writing a new classifier from scratch or changing the scikit-learn implementation. TO-DO: find permanent
            resolution to this issue (raise as an issue on sklearn GitHub?)


    Parameters
    ----------
    n_neighbors     : int, set k for knn (default =1)
    weights         : mechanism for weighting a vote: 'uniform', 'distance' or a callable function: default ==' uniform'
    algorithm       : search method for neighbours {‘auto’, ‘ball_tree’, ‘kd_tree’, ‘brute’}: default = 'brute'
    metric          : distance measure for time series: {'dtw','ddtw','wdtw','lcss','erp','msm','twe'}: default ='dtw'
    metric_params   : dictionary for metric parameters: default = None

    """
    def __init__(self, n_neighbors=1, weights='uniform', algorithm='brute', metric='dtw', metric_params=None, **kwargs):

        self._cv_for_params = False

        if metric == 'dtw':
            metric = dtw_distance
        elif metric == 'dtwcv':  # special case to force loocv grid search cv in training
            if metric_params is not None:
                warnings.warn("Warning: measure parameters have been specified for dtwcv. "
                                     "These will be ignored and parameter values will be found using LOOCV.")
            metric = dtw_distance
            self._cv_for_params = True
            self._param_matrix = {'metric_params': [{'w': x / 100} for x in range(0, 100)]}
        elif metric == 'ddtw':
            metric = ddtw_distance
        elif metric == 'wdtw':
            metric = wdtw_distance
        elif metric == 'wddtw':
            metric = wddtw_distance
        elif metric == 'lcss':
            metric = lcss_distance
        elif metric == 'erp':
            metric = erp_distance
        elif metric == 'msm':
            metric = msm_distance
        elif metric == 'twe':
            metric = twe_distance
        elif metric == 'mpdist':
            metric = mpdist
        # When mpdist is used, the subsequence length (parameter m) must be set
        # Example: knn_mpdist = KNeighborsTimeSeriesClassifier(metric='mpdist', metric_params={'m':30})
        else:
            if type(metric) is str:
                raise ValueError("Unrecognised distance measure: "+metric+". Allowed values are names from [dtw,ddtw,wdtw,wddtw,lcss,erp,msm] or "
                                                                          "please pass a callable distance measure into the constuctor directly.")

        super().__init__(
            n_neighbors=n_neighbors,
            algorithm=algorithm,
            metric=metric,
            metric_params=metric_params,
            **kwargs)
        self.weights = _check_weights(weights)

    def fit(self, X, y):
        """Fit the model using X as training data and y as target values

        Parameters
        ----------
        X : sktime-format pandas dataframe with shape([n_cases,n_dimensions]),
        or numpy ndarray with shape([n_cases,n_readings,n_dimensions])

        y : {array-like, sparse matrix}
            Target values of shape = [n_samples]

        """
        X = check_data_sktime_tsc(X)

        # if internal cv is desired, the relevant flag forces a grid search to evaluate the possible values,
        # find the best, and then set this classifier's params to match
        if self._cv_for_params:
            grid = GridSearchCV(
                estimator=KNeighborsTimeSeriesClassifier(metric=self.metric, n_neighbors=1, algorithm="brute"),
                param_grid=self._param_matrix,
                cv=LeaveOneOut(),
                scoring='accuracy'
            )
            grid.fit(X, y)
            self.metric_params = grid.best_params_['metric_params']

        if y.ndim == 1 or y.ndim == 2 and y.shape[1] == 1:
            if y.ndim != 1:
                warnings.warn("A column-vector y was passed when a 1d array "
                              "was expected. Please change the shape of y to "
                              "(n_samples, ), for example using ravel().",
                              DataConversionWarning, stacklevel=2)

            self.outputs_2d_ = False
            y = y.reshape((-1, 1))
        else:
            self.outputs_2d_ = True

        check_classification_targets(y)
        self.classes_ = []
        self._y = np.empty(y.shape, dtype=np.int)
        for k in range(self._y.shape[1]):
            classes, self._y[:, k] = np.unique(y[:, k], return_inverse=True)
            self.classes_.append(classes)

        if not self.outputs_2d_:
            self.classes_ = self.classes_[0]
            self._y = self._y.ravel()

        temp = check_array.__code__
        check_array.__code__ = _check_array_ts.__code__
        fx = self._fit(X)
        check_array.__code__ = temp
        return fx

    def kneighbors(self, X, n_neighbors=None, return_distance=True):

        """Finds the K-neighbors of a point.
        Returns indices of and distances to the neighbors of each point.

        Parameters
        ----------
        X : sktime-format pandas dataframe with shape([n_cases,n_dimensions]),
        or numpy ndarray with shape([n_cases,n_readings,n_dimensions])

        y : {array-like, sparse matrix}
            Target values of shape = [n_samples]

        n_neighbors : int
            Number of neighbors to get (default is the value
            passed to the constructor).

        return_distance : boolean, optional. Defaults to True.
            If False, distances will not be returned

        Returns
        -------
        dist : array
            Array representing the lengths to points, only present if
            return_distance=True

        ind : array
            Indices of the nearest points in the population matrix.

        Examples
        --------
        In the following example, we construct a NeighborsClassifier
        class from an array representing our data set and ask who's
        the closest point to [1,1,1]

        >>> samples = [[0., 0., 0.], [0., .5, 0.], [1., 1., .5]]
        >>> from sklearn.neighbors import NearestNeighbors
        >>> neigh = NearestNeighbors(n_neighbors=1)
        >>> neigh.fit(samples) # doctest: +ELLIPSIS
        NearestNeighbors(algorithm='auto', leaf_size=30, ...)
        >>> print(neigh.kneighbors([[1., 1., 1.]])) # doctest: +ELLIPSIS
        (array([[0.5]]), array([[2]]))

        As you can see, it returns [[0.5]], and [[2]], which means that the
        element is at distance 0.5 and is the third element of samples
        (indexes start at 0). You can also query for multiple points:

        >>> X = [[0., 1., 0.], [1., 0., 1.]]
        >>> neigh.kneighbors(X, return_distance=False) # doctest: +ELLIPSIS
        array([[1],
               [2]]...)

        """
        check_data_sktime_tsc(X)
        check_is_fitted(self, "_fit_method")

        if n_neighbors is None:
            n_neighbors = self.n_neighbors
        elif n_neighbors <= 0:
            raise ValueError(
                "Expected n_neighbors > 0. Got %d" %
                n_neighbors
            )
        else:
            if not np.issubdtype(type(n_neighbors), np.integer):
                raise TypeError(
                    "n_neighbors does not take %s value, "
                    "enter integer value" %
                    type(n_neighbors))

        if X is not None:
            query_is_train = False
            X = check_array(X, accept_sparse='csr', allow_nd=True)
        else:
            query_is_train = True
            X = self._fit_X
            # Include an extra neighbor to account for the sample itself being
            # returned, which is removed later
            n_neighbors += 1

        train_size = self._fit_X.shape[0]
        if n_neighbors > train_size:
            raise ValueError(
                "Expected n_neighbors <= n_samples, "
                " but n_samples = %d, n_neighbors = %d" %
                (train_size, n_neighbors)
            )
        n_samples = X.shape[0]
        sample_range = np.arange(n_samples)[:, None]

        n_jobs = effective_n_jobs(self.n_jobs)
        if self._fit_method == 'brute':

            reduce_func = partial(self._kneighbors_reduce_func,
                                  n_neighbors=n_neighbors,
                                  return_distance=return_distance)

            # for efficiency, use squared euclidean distances
            kwds = ({'squared': True} if self.effective_metric_ == 'euclidean'
                    else self.effective_metric_params_)

            result = pairwise_distances_chunked(
                X, self._fit_X, reduce_func=reduce_func,
                metric=self.effective_metric_, n_jobs=n_jobs,
                **kwds)

        elif self._fit_method in ['ball_tree', 'kd_tree']:
            if issparse(X):
                raise ValueError(
                    "%s does not work with sparse matrices. Densify the data, "
                    "or set algorithm='brute'" % self._fit_method)
            if LooseVersion(joblib_version) < LooseVersion('0.12'):
                # Deal with change of API in joblib
                delayed_query = delayed(self._tree.query,
                                        check_pickle=False)
                parallel_kwargs = {"backend": "threading"}
            else:
                delayed_query = delayed(self._tree.query)
                parallel_kwargs = {"prefer": "threads"}
            result = Parallel(n_jobs, **parallel_kwargs)(
                delayed_query(
                    X[s], n_neighbors, return_distance)
                for s in gen_even_slices(X.shape[0], n_jobs)
            )
        else:
            raise ValueError("internal: _fit_method not recognized")

        if return_distance:
            dist, neigh_ind = zip(*result)
            result = np.vstack(dist), np.vstack(neigh_ind)
        else:
            result = np.vstack(result)

        if not query_is_train:
            return result
        else:
            # If the query data is the same as the indexed data, we would like
            # to ignore the first nearest neighbor of every sample, i.e
            # the sample itself.
            if return_distance:
                dist, neigh_ind = result
            else:
                neigh_ind = result

            sample_mask = neigh_ind != sample_range

            # Corner case: When the number of duplicates are more
            # than the number of neighbors, the first NN will not
            # be the sample, but a duplicate.
            # In that case mask the first duplicate.
            dup_gr_nbrs = np.all(sample_mask, axis=1)
            sample_mask[:, 0][dup_gr_nbrs] = False

            neigh_ind = np.reshape(
                neigh_ind[sample_mask], (n_samples, n_neighbors - 1))

            if return_distance:
                dist = np.reshape(
                    dist[sample_mask], (n_samples, n_neighbors - 1))
                return dist, neigh_ind
            return neigh_ind

    def predict(self, X):

        """Predict the class labels for the provided data

        Parameters
        ----------
        X : sktime-format pandas dataframe or array-like, shape (n_query, n_features), \
                or (n_query, n_indexed) if metric == 'precomputed'
            Test samples.

        Returns
        -------
        y : array of shape [n_samples] or [n_samples, n_outputs]
            Class labels for each data sample.
        """
        X = check_data_sktime_tsc(X)
        temp = check_array.__code__
        check_array.__code__ = _check_array_ts.__code__
        neigh_dist, neigh_ind = self.kneighbors(X)
        classes_ = self.classes_
        _y = self._y
        if not self.outputs_2d_:
            _y = self._y.reshape((-1, 1))
            classes_ = [self.classes_]

        n_outputs = len(classes_)
        n_samples = X.shape[0]
        weights = _get_weights(neigh_dist, self.weights)

        y_pred = np.empty((n_samples, n_outputs), dtype=classes_[0].dtype)
        for k, classes_k in enumerate(classes_):
            if weights is None:
                mode, _ = stats.mode(_y[neigh_ind, k], axis=1)
            else:
                mode, _ = weighted_mode(_y[neigh_ind, k], weights, axis=1)

            mode = np.asarray(mode.ravel(), dtype=np.intp)
            y_pred[:, k] = classes_k.take(mode)

        if not self.outputs_2d_:
            y_pred = y_pred.ravel()

        check_array.__code__ = temp
        return y_pred

    def predict_proba(self, X):
        """Return probability estimates for the test data X.

        Parameters
        ----------
        X : sktime-format pandas dataframe or array-like, shape (n_query, n_features), \
                or (n_query, n_indexed) if metric == 'precomputed'
            Test samples.

        Returns
        -------
        p : array of shape = [n_samples, n_classes], or a list of n_outputs
            of such arrays if n_outputs > 1.
            The class probabilities of the input samples. Classes are ordered
            by lexicographic order.
        """
        X = check_data_sktime_tsc(X)
        temp = check_array.__code__
        check_array.__code__ = _check_array_ts.__code__

        X = check_array(X, accept_sparse='csr')

        neigh_dist, neigh_ind = self.kneighbors(X)

        classes_ = self.classes_
        _y = self._y
        if not self.outputs_2d_:
            _y = self._y.reshape((-1, 1))
            classes_ = [self.classes_]

        n_samples = X.shape[0]

        weights = _get_weights(neigh_dist, self.weights)
        if weights is None:
            weights = np.ones_like(neigh_ind)

        all_rows = np.arange(X.shape[0])
        probabilities = []
        for k, classes_k in enumerate(classes_):
            pred_labels = _y[:, k][neigh_ind]
            proba_k = np.zeros((n_samples, classes_k.size))

            # a simple ':' index doesn't work right
            for i, idx in enumerate(pred_labels.T):  # loop is O(n_neighbors)
                proba_k[all_rows, idx] += weights[:, i]

            # normalize 'votes' into real [0,1] probabilities
            normalizer = proba_k.sum(axis=1)[:, np.newaxis]
            normalizer[normalizer == 0.0] = 1.0
            proba_k /= normalizer

            probabilities.append(proba_k)

        if not self.outputs_2d_:
            probabilities = probabilities[0]

        check_array.__code__ = temp
        return probabilities


def check_data_sktime_tsc(X):
    """ A utility method to check the input of a TSC KNN classifier. The data must either be in

            a)  the standard sktime format (pandas dataframe with n rows and d columns for n cases with d dimesions)

            OR

            b)  a numpy ndarray with shape([n_cases,n_readings,n_dimensions]) to match the expected format for cython
                distance mesures.

        If the data matches a it will be transformed into b) and returned. If it is already in b), the input X will be
        returned without modification.

        Parameters
        -------
        X : sktime-format pandas dataframe with shape([n_cases,n_dimensions]),
        or numpy ndarray with shape([n_cases,n_readings,n_dimensions])

        y : {array-like, sparse matrix}
            Target values of shape = [n_samples]

        dim_to_use: indesx of the dimension to use (defaults to 0, i.e. first dimension)

        Returns
        -------
        X : numpy ndarray with shape([n_cases,n_readings,n_dimensions])

    """
    if type(X) is pd.DataFrame:
        if X.shape[1] > 1:
            raise TypeError("This classifier currently only supports univariate time series")
        X = np.array([np.asarray([x]).reshape(len(x), 1) for x in X.iloc[:, 0]])
    elif type(X) == np.ndarray:
        try:
            num_cases, num_readings, n_dimensions = X.shape
        except ValueError:
            raise ValueError("X should be a numpy array with 3 dimensions "
                             "([n_cases,n_readings,n_dimensions]). Instead, found: " + str(X.shape))
    return X

def _check_array_ts(array, accept_sparse=False, accept_large_sparse=True,
                    dtype="numeric", order=None, copy=False, force_all_finite=True,
                    ensure_2d=True, allow_nd=True, ensure_min_samples=1,
                    ensure_min_features=1, warn_on_dtype=False, estimator=None):
    return array
