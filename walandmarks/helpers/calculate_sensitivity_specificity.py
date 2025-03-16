"""
Contains manual function for calculating sensitivity and specificity 
from a multiclass confusion matrix.
"""

import numpy as np

def weighted_sensitivity_specificity(confusion):
    """
    Calculates weighted sensitivity and specificity from a multiclass confusion matrix.

    Parameters:
        confusion (np.ndarray): Multiclass confusion matrix.

    Returns:
        tuple: (weighted_sensitivity, weighted_specificity)
    """
    confusion = np.array(confusion)
    num_classes = confusion.shape[0]
    sensitivity = np.zeros(num_classes)
    specificity = np.zeros(num_classes)
    support = np.sum(confusion, axis=1)
    total_samples = np.sum(confusion)

    for i in range(num_classes):
        true_pos = confusion[i, i]
        false_neg = np.sum(confusion[i, :]) - true_pos
        false_pos = np.sum(confusion[:, i]) - true_pos
        true_neg = np.sum(confusion) - true_pos - false_neg - false_pos

        sensitivity[i] = true_pos / (true_pos + false_neg) if (true_pos + false_neg) > 0 else 0
        specificity[i] = true_neg / (true_neg + false_pos) if (true_neg + false_pos) > 0 else 0

    weighted_sensitivity = np.sum(sensitivity * support) / total_samples if total_samples > 0 else 0
    weighted_specificity = np.sum(specificity * support) / total_samples if total_samples > 0 else 0

    return weighted_sensitivity, weighted_specificity
