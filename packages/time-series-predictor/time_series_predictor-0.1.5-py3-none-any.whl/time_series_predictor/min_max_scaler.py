"""
min_max_scaler
"""

import numpy as np

class MinMaxScaler:
    """
    Min Max Scaler class
    """
    def __init__(self):
        self.max = None
        self.min = None

    def fit(self, input_matrix, axis=(0, 1)):
        """Compute the minimum and maximum to be used for later scaling.

        :param input_matrix: input matrix
        :param axis: None or int or tuple of ints, optional Axis or axes along which to operate.
        """
        self.max = np.max(input_matrix, axis=axis)
        self.min = np.min(input_matrix, axis=axis)

    def fit_transform(self, input_matrix):
        """Fit to data, then transform it.

        :param input_matrix: input matrix
        :returns: transformed matrix
        """
        self.fit(input_matrix)
        return self.transform(input_matrix)

    def transform(self, input_matrix):
        """Scale features of input_matrix according to feature_range.

        :param input_matrix: input matrix
        :returns: transformed matrix
        """
        return (input_matrix - self.min) / (self.max - self.min + np.finfo(float).eps)
