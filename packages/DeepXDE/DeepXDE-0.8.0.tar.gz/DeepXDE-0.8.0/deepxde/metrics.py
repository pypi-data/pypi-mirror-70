from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from . import config


def accuracy(y_true, y_pred):
    return np.mean(np.equal(np.argmax(y_pred, axis=-1), np.argmax(y_true, axis=-1)))


def l2_relative_error(y_true, y_pred):
    return np.linalg.norm(y_true - y_pred) / np.linalg.norm(y_true)


def _absolute_percentage_error(y_true, y_pred):
    return 100 * np.abs(
        (y_true - y_pred) / np.clip(np.abs(y_true), np.finfo(config.real(np)).eps, None)
    )


def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(_absolute_percentage_error(y_true, y_pred))


def max_absolute_percentage_error(y_true, y_pred):
    return np.amax(_absolute_percentage_error(y_true, y_pred))


def absolute_percentage_error_std(y_true, y_pred):
    return np.std(_absolute_percentage_error(y_true, y_pred))


def get(identifier):
    metric_identifier = {
        "accuracy": accuracy,
        "l2 relative error": l2_relative_error,
        "MAPE": mean_absolute_percentage_error,
        "max APE": max_absolute_percentage_error,
        "APE SD": absolute_percentage_error_std,
    }

    if isinstance(identifier, str):
        return metric_identifier[identifier]
    elif callable(identifier):
        return identifier
    else:
        raise ValueError("Could not interpret metric function identifier:", identifier)
