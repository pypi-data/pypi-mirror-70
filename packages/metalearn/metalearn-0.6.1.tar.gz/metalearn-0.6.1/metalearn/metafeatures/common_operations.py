import numpy as np

from scipy.stats import skew, kurtosis

import metalearn.metafeatures.constants as consts


def profile_distribution(data):
    """
    Compute the mean, standard deviation, min, quartile1, quartile2, quartile3, and max of a vector

    Parameters
    ----------
    data: array of real values

    Returns
    -------
    features = dictionary containing the min, max, mean, and standard deviation
    """
    if len(data) == 0:
        return (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)
    else:
        ddof = 1 if len(data) > 1 else 0
        dist_mean = np.mean(data)
        dist_stdev = np.std(data, ddof=ddof)
        dist_min, dist_quartile1, dist_quartile2, dist_quartile3, dist_max = np.percentile(data, [0,25,50,75,100])
        dist_skew = skew(data)
        dist_kurtosis = kurtosis(data)
    return (dist_mean, dist_stdev, dist_skew, dist_kurtosis, dist_min, dist_quartile1, dist_quartile2, dist_quartile3, dist_max)

def get_numeric_features(dataframe, column_types):
    return [feature for feature in dataframe.columns if column_types[feature] == consts.NUMERIC]

def get_categorical_features(dataframe, column_types):
    return [feature for feature in dataframe.columns if column_types[feature] == consts.CATEGORICAL]

def dtype_is_numeric(dtype):
    return "int" in str(dtype) or "float" in str(dtype)
